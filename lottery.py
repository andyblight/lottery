"""
TODO
Frequency count for date ranges.

"""
import csv
import datetime


main_balls = []
lucky_stars = []

def frequency(max_num, ball_list):
    # print(ball_list)
    frequency_of_balls = []
    for ball_number in range(1, max_num + 1):
        ball_count = 0
        for ball in ball_list:
            # print(ball_number, ball_count, ball)
            if ball_number == int(ball):
                ball_count += 1
        frequency_of_balls.append((ball_number, ball_count))
    print(frequency_of_balls)

def convert_str_to_date(date_str):
    formatter_string = "%d-%b-%Y" 
    date_object = datetime.datetime.strptime(date_str, formatter_string).date()
    return date_object

def frequency_in_date_range(filereader, date_from_str, date_to_str):
    print("From", date_from_str, "to", date_to_str)
    date_from = convert_str_to_date(date_from_str)
    date_to = convert_str_to_date(date_to_str)
    print("Converted: From", date_from, "to", date_to)
    #for row in filereader:
#        row_date = date
#        if (row[0] )
#            print(row)

def process_data(filereader):
    frequency_in_date_range(filereader, "23-Jan-2017", "23-Feb-2017")
    frequency(50, main_balls)
    frequency(12, lucky_stars)

def run(filename):
    with open(filename, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        process_data(filereader)

if __name__ == "__main__":
    # execute only if run as a script
    run('euromillions-draw-history.csv')
