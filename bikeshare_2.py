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
    print('Hello! Let\'s digg into some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = CITY_DATA.keys()

    while True:
        try:
            city = input('\nPlease select the city you want to explore. Available cities are: Chicago, New York City, and Washington:\n').lower()
        except:
            print('No valid input. Please try again')
            continue

        if city not in cities:
            print('Data for {} is not available. Please try again.'.format(city))
            continue
        else:
            break


    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        try:
            month = input('\nPlease select the month you want to filter by (January - June). If you don\'t want to filter by month select all:\n').lower()
        except:
            print('No valid input. Please try again')
            continue

        if month not in months:
            print('Data for {} is not available. Please try again'.format(month))
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        try:
            day = input('\nPlease select the day of the week you want to filter by. Please type in the full name of the day (e.g. Monday). If you don\'t want to filter by day select all:\n').lower()
        except:
            print('No valid input. Please try again')
            continue

        if day not in days:
            print('Data for {} is not available.Please try again'.format(day))
            continue
        else:
            break

    print('\nYour filter settings are:\nCity: {}\nMonth: {}\nDay: {}\n'.format(city.title(), month.title(), day.title()))
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]
    print('Most popular month:', months[popular_month - 1].title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end)

    # display most frequent combination of start station and end station trip
    df['Trip'] = 'From: ' + df['Start Station'] + ' To: ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most popular trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Travel Time'] = df['End Time'] - df['Start Time']

    # display total travel time
    total_travel_time = df['Travel Time'].sum().seconds / 60
    print('Total travel time: ', total_travel_time, 'minutes')

    # display mean travel time
    mean_travel_time = df['Travel Time'].mean().seconds / 60
    print('Mean travel time: ', mean_travel_time, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:')
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('\nCounts of gender:')
        print(genders)
    else:
        print('\nNo gender data available')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        e_yob = df['Birth Year'].min()
        print('\nOldest customer born in:', int(e_yob))
        r_yob = df['Birth Year'].max()
        print('Youngest customer born in', int(r_yob))
        c_yob = df['Birth Year'].mode()[0]
        print('Most common year of birth:', int(c_yob))
    else:
        print('No gender data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    while True:
        raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if raw.lower() != 'yes':
            break
        else:
            print(df.head(5))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
