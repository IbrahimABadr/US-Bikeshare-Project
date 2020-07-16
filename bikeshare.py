import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Ready! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please select your city from: chicago, new york city, washington\n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Oops!, Invalid city choice try again.\n")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please select your month from: january, february, march, april, may, june, all\n").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Oops!, Invalid month choice try again.\n")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please select your day from: sunday ,monday ,tuesday, wednesday, thursday, friday, saturday, all\n").lower()
        if day not in ('sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'):
            print("Oops!, Invalid day choice try again.\n")
            continue
        else:
            break


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
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
    popular_month = df['month'].mode()[0]
    print('-Most common month      :', popular_month)
    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('-Most common day Of week:', popular_day_of_week)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('-Most common hour of day:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('-Most common start station       : {}\n'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('-Most common end station         : {}\n'.format(common_end_station))
    # display most frequent combination of start station and end station trip
    frequent_combin_trip = df['Start Station'].astype(str) + " to " + df['End Station'].astype(str)
    combin_frequent_trip = frequent_combin_trip.value_counts().idxmax()
    print('-Most frequent combined trip from: {}\n'.format(combin_frequent_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (total_travel_time/86400)
    print('-Total travel time  :', total_travel_time, " days")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (mean_travel_time/60)
    print('-Average travel time:', mean_travel_time, " min")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    no_of_subscribers = df['User Type'].str.count('Subscriber').sum()
    no_of_customers = df['User Type'].str.count('Customer').sum()
    print('-No. of subscribers    : {}\n'.format(int(no_of_subscribers)))
    print('-No. of customers      : {}\n'.format(int(no_of_customers)))

    # Display counts of gender
    if('Gender' in df):
        male_count = df['Gender'].str.count('Male').sum()
        female_count = df['Gender'].str.count('Female').sum()
        print('-No. of male users     : {}\n'.format(int(male_count)))
        print('-No. of female users   : {}\n'.format(int(female_count)))
    else:
        print("-No. of male users     : Not available")
        print("-No. of female users   : Not available")

    # Display earliest, most recent, and most common year of birth
    if('Birth Year' in df):
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print("-Earliest birth year   : {}\n".format(int(earliest_year)))
        print("-Recent birth year     : {}\n".format(int(most_recent_year)))
        print("-Most common birth year: {}\n".format(int(common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    raw_data = 0
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data_sample = input('\nWould you like to see raw data sample? Enter (yes or no)\n')
        if raw_data_sample.lower() == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])

        restart = input('\nWould you like to restart? Enter (yes or no), and remeber Stay Safe\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
