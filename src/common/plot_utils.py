import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

FULL_COLUMNS    = ['time', 'x', 'y', 'x_dot', 'y_dot', 'x_double_dot', 'y_double_dot', 'force_x', 'force_y']

plt.rcParams.update({'font.size': 5})
plt.rcParams['lines.linewidth'] = 2

def separate_upper_and_lower_tubes(reach_tube):
    upper_bound = [reach_tube[0]]
    lower_bound = [reach_tube[0]]

    i = 1
    while i < len(reach_tube)-1:
        upper_bound.append(reach_tube[i])
        i += 1
        lower_bound.append(reach_tube[i])
        i += 1

    upper_bound.append(reach_tube[len(reach_tube)-1])
    lower_bound.append(reach_tube[len(reach_tube)-1])

    return upper_bound, lower_bound

def plot_varibles_vs_time(upper,lower):
    upper_df = pd.DataFrame(upper, columns=FULL_COLUMNS)
    lower_df = pd.DataFrame(lower, columns=FULL_COLUMNS)
    time     = upper_df['time']

    fig, axes = plt.subplots(4,2,sharex=True)

    axes[0,0].plot(time, upper_df['x'], 'k')
    axes[0,0].plot(time, lower_df['x'], 'k')
    axes[0,0].fill_between(time, lower_df['x'], upper_df['x'], linewidth=50)
    axes[0,0].set_ylabel('x Pos (m)')
    axes[0,0].set_title('Simulation Variables vs Time', fontsize=12)

    axes[1,0].plot(time, upper_df['y'], 'k')
    axes[1,0].plot(time, lower_df['y'], 'k')
    axes[1,0].fill_between(time, lower_df['y'], upper_df['y'])
    axes[1,0].set_ylabel('y Pos (m)')

    axes[2,0].plot(time, upper_df['x_dot'], 'k')
    axes[2,0].plot(time, lower_df['x_dot'], 'k')
    axes[2,0].fill_between(time, lower_df['x_dot'], upper_df['x_dot'])
    axes[2,0].set_ylabel('x Vel (m/s)')

    axes[3,0].plot(time, upper_df['y_dot'], 'k')
    axes[3,0].plot(time, lower_df['y_dot'], 'k')
    axes[3,0].fill_between(time, lower_df['y_dot'], upper_df['y_dot'])
    axes[3,0].set_ylabel('y Vel (m/s)')
    axes[3,0].set_xlabel('Time (sec)', fontsize=10)

    axes[0,1].plot(time, upper_df['x_double_dot'], 'k')
    axes[0,1].plot(time, lower_df['x_double_dot'], 'k')
    axes[0,1].fill_between(time, lower_df['x_double_dot'], upper_df['x_double_dot'])
    axes[0,1].set_ylabel('x Acc (m/s**2)')
    axes[0,1].set_title('Simulation Variables vs Time', fontsize=12)

    axes[1,1].plot(time, upper_df['y_double_dot'], 'k')
    axes[1,1].plot(time, lower_df['y_double_dot'], 'k')
    axes[1,1].fill_between(time, lower_df['y_double_dot'], upper_df['y_double_dot'])
    axes[1,1].set_ylabel('y Acc (m/s**2)')

    axes[2,1].plot(time, upper_df['force_x'], 'k')
    axes[2,1].plot(time, lower_df['force_x'], 'k')
    axes[2,1].fill_between(time, lower_df['force_x'], upper_df['force_x'])
    axes[2,1].set_ylabel('x Force (N)')

    axes[3,1].plot(time, upper_df['force_y'], 'k')
    axes[3,1].plot(time, lower_df['force_y'], 'k')
    axes[3,1].fill_between(time, lower_df['force_y'], upper_df['force_y'])
    axes[3,1].set_ylabel('y Force (N)')
    axes[3,1].set_xlabel('Time (sec)', fontsize=10)

    plt.tight_layout()
    fig.savefig('output/variables_vs_time.png')

def define_axes(df1, df2):
    max_x = max(df1['x'].max(), df2['x'].max()) * 1.05
    min_x = min(-500, min(df1['x'].min(), df2['x'].min())) * 1.05
    max_y = max(df1['y'].max(), df2['y'].max()) * 1.05
    min_y = min(-500, min(df1['y'].min(), df2['y'].min())) * 1.05
    return (min_x, max_x, min_y, max_y)

def create_target():
    return plt.Circle((0,0), 100, color='g')

def create_radius(radius):
    return plt.Circle((0,0), radius, color='r', fill=False)

def plot_simulation(upper, lower):
    upper_df = pd.DataFrame(upper, columns=FULL_COLUMNS)
    lower_df = pd.DataFrame(lower, columns=FULL_COLUMNS)

    min_x, max_x, min_y, max_y = define_axes(upper_df, lower_df)
    target = create_target()
    radius = create_radius(1000)

    fig, ax = plt.subplots()
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.add_artist(target)
    ax.add_artist(radius)
    ax.scatter(upper_df['x'], upper_df['y'], c='r', s=1)
    ax.scatter(lower_df['x'], lower_df['y'], c='b', s=1)

    ax.set_title('Simulation Position in 2D Space', fontsize=12)
    ax.set_xlabel('x Position (m)', fontsize=10)
    ax.set_ylabel('y Position (m)', fontsize=10)
    ax.legend(['Upper Tube', 'Lower Tube'], fontsize=8)
    plt.tight_layout()
    plt.savefig('output/simulation_position.png')

def add_rho_position(df):
    df['rho_position'] = np.sqrt(df['x']**2 + df['y']**2)
    return df

def add_total_velocity(df):
    df['tot_vel'] = np.sqrt(df['x_dot']**2 + df['y_dot']**2)
    return df

def add_total_acceleration(df):
    df['tot_acc'] = np.sqrt(df['x_double_dot']**2 + df['y_double_dot']**2)
    return df

def add_total_force(df):
    df['tot_force'] = np.sqrt(df['force_x']**2 + df['force_y']**2)
    return df

def add_variables(df):
    df = add_rho_position(df)
    df = add_total_velocity(df)
    df = add_total_acceleration(df)
    df = add_total_force(df)
    return df

def plot_other_varialbes_vs_time(upper, lower):
    upper_df = pd.DataFrame(upper, columns=FULL_COLUMNS)
    lower_df = pd.DataFrame(lower, columns=FULL_COLUMNS)
    time     = upper_df['time']

    upper_df = add_variables(upper_df)
    lower_df = add_variables(lower_df)

    fig, axes = plt.subplots(4,1,sharex=True)

    axes[0].plot(time, upper_df['rho_position'], 'k')
    axes[0].plot(time, lower_df['rho_position'], 'k')
    axes[0].fill_between(time, lower_df['rho_position'], upper_df['rho_position'])
    axes[0].set_title('Computed Variables vs Time', fontsize=12)
    axes[0].set_ylabel('Rho (m)')

    axes[1].plot(time, upper_df['tot_vel'], 'k')
    axes[1].plot(time, lower_df['tot_vel'], 'k')
    axes[1].fill_between(time, lower_df['tot_vel'], upper_df['tot_vel'])
    axes[1].set_ylabel('Total Vel (m/s)')

    axes[2].plot(time, upper_df['tot_acc'], 'k')
    axes[2].plot(time, lower_df['tot_acc'], 'k')
    axes[2].fill_between(time, lower_df['tot_acc'], upper_df['tot_acc'])
    axes[2].set_ylabel('Total Accl (m/s**2)')

    axes[3].plot(time, upper_df['tot_force'], 'k')
    axes[3].plot(time, lower_df['tot_force'], 'k')
    axes[3].fill_between(time, lower_df['tot_force'], upper_df['tot_force'])
    axes[3].set_ylabel('Total Force (N)')

    plt.xlabel('Time (sec)', fontsize=10)
    plt.tight_layout()
    fig.savefig('output/other_variables_vs_time.png')
