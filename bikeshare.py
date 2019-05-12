import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
   Asks user to specify a city, month, and day to analyze.

   Returns:
       (str) city - name of the city to analyze
       (str) month - name of the month to filter by, or "all" to apply no month filter
       (str) day - name of the day of week to filter by, or "all" to apply no day filter
   """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Gets user input for city (chicago, new york city, washington, uses while loop for invalid
    city_name = input('Would you like to see data for Chicago, New York, or Washington?: ').lower()

    while city_name not in ['chicago', 'new york city', 'washington']:
        print('Please enter a valid city')
        city_name = input('Choose a city between Chicago,New York City and Washington: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input(
        'Choose a month to explore between Jan and Jun. If you want to explore all months please enter all: ').lower()

    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print('Please enter a valid month')
        month = input(
            ' Please enter a valid month betwen jan and juen. To look at all months please enter all: ').lower()

    # Gets user input for day of week (all, monday, tuesday, sunday)
    day = input('Which day would you like to explore ? If you want to look at all days please enter all: ').lower()

    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print('Please enter a valid day')
        day = input(' Please enter the 3 letter day shortform.To look at all days please enter all: ').lower()

    print('-' * 40)
    return city_name, month, day


def load_data(city, month, day):
    # print("Dictionary selection:  ",CITY_DATA[city])
    # loads data file into a data frame
    try:
        # print('start reading the data')
        df = pd.read_csv(CITY_DATA[city])
        # Ends reading the data
    except Exception as e:
        print(e)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of the Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commonly_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', commonly_start_station)

    # display most commonly used end station
    commonly_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', commonly_end_station)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    station_combination = df['combination'].mode()[0]

    print('Most common Combination:', station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total travel Time for the city is:', total_travel_time)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()

    print('The mean of the travel Time:', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()

    print('Count of user types:', count_user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Counts of gender:', gender)
    else:
        print("Gender information is not available for this city!")

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest year of birth for these users:', earliest_birth_year)

        recent_birth_year = df['Birth Year'].max()
        print('Recent year of birth:', recent_birth_year)

        common_birth_year = df['Birth Year'].mode()[0]
        print('Most common year of birth', common_birth_year)
        print('')
    else:
        print("Birth year information is not available for this city!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def data(df):
    """Displays 5 rows of raw data at a time"""
    row_number = 0
    print("\nDo you want to see raw data?\n")
    user_answer = input("Yes or no?\n").lower()
    if user_answer not in ['yes', 'no']:
        print("\nThe answer is not valid\n")
    elif user_answer == 'yes':
        while True:
            row_number += 5
            print(df.iloc[row_number: row_number + 5])
            print("\nDo you want to see more raw data?\n")
            continues = input("Yes or no?\n").strip().lower()
            if continues == 'no':
                break
    elif user_answer == 'yes':
        return df.iloc[row_number: row_number + 5]


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
