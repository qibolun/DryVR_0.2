def calculate_double_dots(df):
    time = dt.datetime.now()
    df.at[0, 'x_double_dot'] = 0
    df.at[0, 'y_double_dot'] = 0
    for i in range(1, df.shape[0]):
        prev_row = df.iloc[i-1]
        curr_row = df.loc[i]
        denom = curr_row['time'] - prev_row['time']
        if denom != 0:
            df.at[i, 'x_double_dot'] = float( (curr_row['x_dot'] - prev_row['x_dot']) / denom )
            df.at[i, 'y_double_dot'] = float( (curr_row['y_dot'] - prev_row['y_dot']) / denom )
        else:
            df.at[i, 'x_double_dot'] = 0
            df.at[i, 'y_double_dot'] = 0
    print '\tCalculated Acceleration:', (dt.datetime.now() - time).total_seconds(), 'seconds'
    return df
