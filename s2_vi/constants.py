import csv

# construct list of all days of the year in the format MM-DD (01-01 to 12-31, including 02-29)
month_lengths = [None, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
days_of_the_year = []
for month in range(1, 12+1):
    for day in range(1, month_lengths[month]+1):
        mm = ("0" if month<10 else "") + str(month)
        dd = ("0" if day<10 else "") + str(day)
        days_of_the_year.append(mm + '-' + dd)

# split that list into before/during/after period for which data is supplied
jan_feb = [x for x in days_of_the_year if x.startswith('01') or x.startswith('02')]
end_oct = ['10-27', '10-28', '10-29', '10-30', '10-31']
nov_dec = [x for x in days_of_the_year if x.startswith('11') or x.startswith('12')]
rest_of_year = [x for x in days_of_the_year if x not in [*jan_feb, *end_oct, *nov_dec]]

# function to read data from a DLR-supplied CSV file
def read_data_from_csv(filename):
    result = {}

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        counter = 0

        for row in reader:
            # setup data structure on first iteration
            if counter == 0:
                for key in row:
                    if key != 'MM-DD':
                        result[key] = {}  # initialise empty objects so that the subsequent loop can just blindly write to them

            # write data in each iteration
            for key in row:
                if key != 'MM-DD':
                    # handle beginning of year on first iteration
                    if counter == 0:
                        for day in jan_feb:
                            result[key][day] = float(row[key])  # just set the first value

                    # always handle normal step: each data point is representative for an interval of five days
                    for i in range(5):
                        day = rest_of_year[counter*5 + i]  # get the current MM-DD from the list
                        result[key][day] = float(row[key])  # set the value

                    # handle end of year in last iteration
                    if counter == 47:
                        for day in [*end_oct, *nov_dec]:
                            result[key][day] = float(row[key])  # just set the last value

            # increase counter
            counter += 1

    # return filled data structure
    return result

# call that function for all data that is needed
ndvi_means = read_data_from_csv('/home/datacube/ows_refactored/s2_vi/DLR_vegetation-indices-multiyear/ndvi_means_2018-2021.csv')
ndvi_stds = read_data_from_csv('/home/datacube/ows_refactored/s2_vi/DLR_vegetation-indices-multiyear/ndvi_stds_2018-2021.csv')
evi_means = read_data_from_csv('/home/datacube/ows_refactored/s2_vi/DLR_vegetation-indices-multiyear/evi_means_2018-2021.csv')
evi_stds = read_data_from_csv('/home/datacube/ows_refactored/s2_vi/DLR_vegetation-indices-multiyear/evi_stds_2018-2021.csv')
