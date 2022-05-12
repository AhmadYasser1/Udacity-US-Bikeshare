import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_DATA = ["no", "january", "february", "march", "april", "may", "june"]

DAYS_DATA = ["no", "saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "no" to apply no month filter
        (str) day - name of the day of week to filter by, or "no" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cityInput = input("Enter the name of the city (Chicago, New York City, Washington): ").lower()
    while cityInput not in CITY_DATA:
        cityInput= input("You entered a wrong city, please enter a city again (Chicago, New York City, Washington): ").lower()

    # get user input for month (no, january, february, ... , june)
    monthInput = input("Enter the month to filter by (from January to June only) or type 'no' for no filter: ").lower()
    while monthInput not in MONTHS_DATA:
        monthInput= input("You entered a wrong month, please enter a month again (from January to June only) or type 'no' for no filter: ").lower()

    # get user input for day of week (no, monday, tuesday, ... sunday)
    dayInput = input("Enter the day of the week to filter by or type 'no' for no filter: ").lower()
    while dayInput not in DAYS_DATA:
        dayInput = input("You entered a wrong day, please enter a day of the week again or type 'no' for no filter: ").lower()

    print('-'*40)
    return cityInput, monthInput, dayInput


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "no" to apply no month filter
        (str) day - name of the day of week to filter by, or "no" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day and hour
    """
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Month"] = df["Start Time"].dt.month # 1, 2, 3, 
    df["Day of Week"] = df["Start Time"].dt.weekday_name # Sunday, Monday
    df["Hour"] = df['Start Time'].dt.hour 

    if month != "no" :
        month = MONTHS_DATA.index(month)
        df = df[df["Month"] == month]
    if day != "no":
        df = df[df["Day of Week"] == day.title()] 
    
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    if month == "no":
        commonMonth = df["Month"].mode()[0]
        print("The most common month is: {}".format(MONTHS_DATA[commonMonth].title()))

    # display the most common day of week
    if day == "no":
        commonDay = df["Day of Week"].mode()[0]
        print("The most common day of the week is: {}".format(commonDay))
        
    # display the most common start hour
    commonHour = df["Hour"].mode()[0]
    print("The most common hour is: {}".format(commonHour))
    
    print("\nThis took {} seconds.".format(round((time.time() - start_time),1)))
    print('-'*40) 


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commonStartStation = df["Start Station"].mode()[0]
    print(f"The most common start station is {commonStartStation}")

    # display most commonly used end station
    commonEndStation = df["End Station"].mode()[0]
    print(f"The most common end station is {commonEndStation}")

    # display most frequent combination of start station and end station trip
    frequentCombination = (df['Start Station'] + '|' + df['End Station']).mode()[0]
    frequentCombination = frequentCombination.split("|")
    print(f"The most frequent combination of start station and end station trip, respectively, is\nStart Station: {frequentCombination[0]}\nEnd Station: {frequentCombination[1]}")

    print("\nThis took {} seconds.".format(round((time.time() - start_time),1)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totalTravelTime = df['Trip Duration'].sum() 
    print(f"The total tavel time is {totalTravelTime} seconds")

    # display mean travel time
    meanTravelTime = df['Trip Duration'].mean() 
    print(f"The mean tavel time is {round(meanTravelTime,1)} seconds")

    print("\nThis took {} seconds.".format(round((time.time() - start_time),1)))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    userTypesCounts = df["User Type"].value_counts()
    print("The counts of user types are {}".format(userTypesCounts))

    # Display counts of gender
    if city != "washington":
        genderCounts = df["Gender"].value_counts()
        print("The counts of gender are {}".format(genderCounts))
        earliestYear = int(df['Birth Year'].min())
        print(f"The earliest year of birth is {earliestYear}")
        recentYear = int(df['Birth Year'].max())
        print(f"The most recent year of birth is {recentYear}")
        commonYear = int(df["Birth Year"].mode()[0])
        print(f"The most common year of birth is {commonYear}")
    else:
        print(f"The counts of gender, earliest year of birth, most recent year of birth, and most common year of birth are unretrievable due to incomplete data.")
    
    print("\nThis took {} seconds.".format(round((time.time() - start_time),1)))
    print('-'*40)

def display_raw_data(df):
    """Displays a sample of the raw data"""

    print("Do you want to take a look at the raw data?\n")
    response = input("Enter yes or no? ").lower()
    next = 0
    pd.set_option('display.max_columns',200)
    while response == "yes":
        print(df.iloc[next:next+5])
        next += 5
        print("Do you want to take another look at the raw data?\n")
        response = input("Enter yes or no? ").lower()
        
    print('-'*40)
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes' and restart == "no":
           break
        else:
            while restart != "yes" or restart != "no":
                if restart != 'yes' and restart == "no":
                    break
                elif restart == "yes":
                    break
                else:
                    restart = input('\nPlease enter an appropriate answer. Enter yes or no.\n').lower()
        if restart != 'yes' and restart == "no":
           break


if __name__ == "__main__":
	main()