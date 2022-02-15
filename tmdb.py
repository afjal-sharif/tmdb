from telegram.ext import Updater,CallbackContext,CommandHandler,MessageHandler,Filters
from telegram import Update
from variables import * 
from constants import *
import requests
import re

#Bot updater inizialization
updater = Updater(token=TAPI_KEY,use_context=True)

#Active Language initialization
active_language = default_language


def start(update: Update, context: CallbackContext) -> None:
    """Callback function for start command.
    Sends a message a welcoming message.
    Will be called when check_update has determined that an update should be processed by the associated handler.
        
        Parameters: 
            update (Update):  an incoming update.
            context (CallbackContext): a context object.
        Returns: 
            None 
    """
    context.bot.sendMessage(chat_id=update.effective_chat.id,text=start_message[active_language])

def help(update: Update, context: CallbackContext) -> None:
    """Callback function for help command.
    Sends a message a help message.
    Will be called when check_update has determined that an update should be processed by the associated handler.
        
        Parameters: 
            update (Update):  an incoming update.
            context (CallbackContext): a context object.
        Returns: 
            None 
    """
    context.bot.sendMessage(chat_id=update.effective_chat.id,text=help_message[active_language])

def language_command(update: Update, context: CallbackContext) -> None:
    """Callback function for language command.
    Change the value of active_language to the one passed as argument to the command if possible, 
    otherwise sends a message with a list of valid languages.
    Will be called when check_update has determined that an update should be processed by the associated handler.
        
        Parameters: 
            update (Update):  an incoming update.
            context (CallbackContext): a context object.
        Returns: 
            None 
    """
    global active_language
    output_string = ''
    new_language = active_language 
    try:
        new_language = context.args[0] if context.args[0] in valid_languages else active_language 
    except:
        output_string = 'Valid arguments for /language : {options}.\nCurrent Language: {curr}'.format(options=' , '.join(valid_languages),curr=active_language)
    finally:
        active_language = new_language
        if output_string: 
            context.bot.sendMessage(chat_id=update.effective_chat.id,text=output_string)

def details(update: Update, context: CallbackContext) -> None:
    """Callback function for details command.
    Sends a message with details of the resource passed as argument to the command if possible. 
    If it's not possible sends a message, otherwise sends a hint on how to use the command. 
    Will be called when check_update has determined that an update should be processed by the associated handler.
        
        Parameters: 
            update (Update):  an incoming update.
            context (CallbackContext): a context object.
        Returns: 
            None 
    """
    #Message string that will be sent
    output_string = ''; 
    #Id of resource we're trying to get details from
    tv_id = None
    
    endpoint_path = ''
    endpoint = ''
    result = {}
    if not context.args:
        #No arguments passed to the command, can't get any details. 
        output_string += 'Usage: /details {tv_series_id | tv_series_name}\n'
        context.bot.sendMessage(chat_id=update.effective_chat.id,text=output_string)
        return
    elif len(context.args) > 1 or not re.match('^[0-9]+$',' '.join(context.args)):
        #TV series name passed as argument to the command, get the id associated and store it inside tv_id variable.
        title = '+'.join(context.args[i].lower() for i in range(len(context.args)))
        endpoint_path = '/search/tv/'
        endpoint = '{api_base_url}{endpoint_path}?api_key={api_key}&language={lang}&query={title}'.format(api_base_url=api_base_url,endpoint_path=endpoint_path,api_key=MDBAPI_KEY,title=title,lang=active_language)
        try:
            tv_id = requests.get(url=endpoint).json()['results'][0]['id']
        except:
            #No tv shows found with the name passed as argument, can't get any details. 
            output_string += 'The resource you requested could not be found.\n'
            context.bot.sendMessage(chat_id=update.effective_chat.id,text=output_string)
            return
    else:
        #TV series id passed as argument to the command, store it inside tv_id variable.
        tv_id = context.args[0]

    endpoint_path = '/tv/{tv_id}'.format(tv_id=str(tv_id))
    endpoint = '{api_base_url}{endpoint_path}?api_key={api_key}&language={lang}'.format(api_base_url=api_base_url,endpoint_path=endpoint_path,api_key=MDBAPI_KEY, lang=active_language)
    result = requests.get(url=endpoint).json()
    
    try: 
        #Get details associated to the tv_id resource and store them inside the output_string variable. 
        output_string += '{name}, ({orig_name})\n{yy} {gnre}\n'.format(name=result['name'],orig_name=result['original_name'],yy=result['first_air_date'] if result['first_air_date'] else '',gnre=' , '.join([d['name'] for d in result['genres']]))
        if result['in_production']:
            output_string += 'In production\n'
        else:
            output_string += 'Not in production\n'
        output_string += '{overview}\n'.format(overview=result['overview'])
    except:
        #Error during request
        output_string += result['status_message']
    finally:
        if output_string: 
            #Send the resource details
            if result['poster_path'] or result['backdrop_path']:
                image = 'https://image.tmdb.org/t/p/original{backdrop_p}'.format(backdrop_p=result['poster_path'] or result['backdrop_path'])
                context.bot.sendPhoto(chat_id=update.effective_chat.id,photo=image)
            context.bot.sendMessage(chat_id=update.effective_chat.id,text=output_string)

def top(update: Update, context: CallbackContext) -> None:
    """Callback function for top command.
    Sends a message with a brief description of the most popular tv shows of the moment. 
    Will be called when check_update has determined that an update should be processed by the associated handler.
        
        Parameters: 
            update (Update):  an incoming update.
            context (CallbackContext): a context object.
        Returns: 
            None 
    """
    endpoint_path = '/tv/popular'
    endpoint = '{api_base_url}{endpoint_path}?api_key={api_key}&language={lang}'.format(api_base_url=api_base_url,endpoint_path=endpoint_path,api_key=MDBAPI_KEY, lang=active_language)

    result = requests.get(url=endpoint).json()["results"]
    
    #Message string that will be sent
    res = ''
    temp = ''
    
    #Store inside res variable top 10 (or less) popular tv shows of the moment
    i = 0
    while i < 10 and i < len(result):
        temp = '# {pos}\n'.format(pos=str(i+1))
        temp += '{title}\n'.format(title=result[i]['name'])
        temp += '{overview}\n'.format(overview=result[i]['overview'])
        temp += 'Rate: {score}\n\n'.format(score=str(result[i]['vote_average']))
        i += 1
        #Check if we've reached the maximum length for a message
        if len(res + temp) > MAX_MESSAGE:
            break
        else:
            res += temp
    context.bot.sendMessage(chat_id=update.effective_chat.id,text=res)

def messages(update: Update, context: CallbackContext) -> None:
    context.bot.sendMessage(chat_id=update.effective_chat.id,text='???')

def main():
    
    #Command Handler List
    chandler_list = [
        CommandHandler('start',start),
        CommandHandler('help',help),
        CommandHandler('details',details),
        CommandHandler('top',top),
        CommandHandler('language',language_command)]

    #Message Handler List
    mhandler_list = [MessageHandler(Filters.text & (~Filters.command),callback=messages)]


    for i in range (len(chandler_list)):
        updater.dispatcher.add_handler(chandler_list[i])
    for i in range (len(mhandler_list)):
        updater.dispatcher.add_handler(mhandler_list[i])

    #Start the bot
    updater.start_polling()
    #Run the bot until Ctrl+C kill him
    updater.idle()

if __name__ == '__main__':
    main()