#Prefix API TMDB
api_base_url = 'https://api.themoviedb.org/3'
#Dictionary of start messages in different languages
start_message = {
    'en':'Are you looking for new TV series / Movies to watch?\nI\'m going to help you!\nUnder the hood I\'m using The Movie Database API (https://developers.themoviedb.org/3).\nYou can start by typing /help for an overview of my commands.',
    'it':'Stai cercando nuove serie TV / film da vedere? Ti aiuterò!\nSotto il cappuccio sto utilizzando le API di The Movie Database(https://developers.themoviedb.org/3).\nPer avere una panoramica dei comandi utilizza /help.'
}
help_message = {
    'en':'Hey! My name is TMDBot. I am here to help you watch interesting shows/movies.\nI\'m a newborn so all of my features are still in development.\n\nHere\'s a list of helpful commands:\n-/start: Start me! Nothing special.\n-/help: The command you just used, don\'t you remember?\n-/top: Sends a short list of the most popular series of the moment.\n-/details {tv_series_name | tv_series_id}: Gives details about the tv series passed as argument of the command.\n-/language {option}: Sets my language. Option should be one of the supported languages.',
    'it':'Hey! Il mio nome è TMDBot. Sono qui per aiutarti a guardare serie/film interessanti.\nSono ancora un neonato quindi le mie funzionalità sono ancora in sviluppo.\n\nEcco qui una lista di comandi utili:\n-/start: Iniziamo! Niente di speciale.\n/help: Il comando che hai appena usato, non ti ricordi?\n-/top: Manda una breve lista delle serie più guardate del momento.\n-/details {nome_serie_tv | id_serie_tv}: Mando dettagli sulla serie tv passata come parametro al comando.\n-/language {opzione}: Setta la mia lingua. Opzione deve essere una delle lingue supportate.' 
}
#Languages list
valid_languages = ['en','it']
default_language = 'it'
#Maximum number of characters in a telegram message
MAX_MESSAGE = 4096