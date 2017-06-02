import csv

main_balls = []
lucky_stars = []

def load_file(filename):
    with open(filename, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        first_row = True
        for row in filereader:
            if first_row:
                first_row = False
                continue
            main_balls.append(row[1])
            main_balls.append(row[2])
            main_balls.append(row[3])
            main_balls.append(row[4])
            main_balls.append(row[5])
            lucky_stars.append(row[6])
            lucky_stars.append(row[7])

def frequency(max_num, ball_list):
    print(ball_list)
    frequency_of_balls = []
    for ball_number in range(1, max_num + 1):
        ball_count = 0
        for ball in ball_list:
            print(ball_number, ball_count, ball)
            if ball_number == int(ball):
                ball_count += 1
        frequency_of_balls.append((ball_number, ball_count))
    print(frequency_of_balls)

if __name__ == "__main__":
    # execute only if run as a script
    load_file('euromillions-draw-history.csv')
    frequency(12, lucky_stars)
