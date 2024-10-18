from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency='USD')
        bot.select_place_to_go(place_to_go=input("Where you want to go?\n"))
        bot.select_dates(check_in_date=input("What is the check in date?\n"), 
                         check_out_date=input("What is the check out date?\n"))
        
        bot.select_adults(count=int(input("How many people?\n")))
        bot.click_search()
        bot.apply_filtrations()
        bot.report_results()

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows \n'
            '   set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux \n'
            '   PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise