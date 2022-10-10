close all
%% 
% Usage:
% 1. Load the data struct into the Workspace (output.mat)
% 2. Run individual sections of the script to plot the desired data
%% Test Plot for Daq Bulkhead Node
% figure
% hold on
% plot(S.roll(:,1)/1000,S.roll(:,2));
% plot(S.heading(:,1)/1000,S.heading(:,2));
% plot(S.pitch(:,1)/1000,S.pitch(:,2));
% 
% legend({'roll', ...
%     'heading','pitch'})
% xlabel('Time (s)')
% title('roll n heading test')
% h = zoom;
% set(h,'Motion','horizontal','Enable','on');
%% Torque, Vehicle Speed, Current, mega plot
figure

uptime=S.rms_uptime;
requested_torque = S.requested_torque;
commanded_torque = S.commanded_torque;
busVoltage = S.dc_bus_voltage;
motor_speed = S.motor_speed;
pedal_data = S.accelerator_pedal_1(:, 2);
pedal_time = S.accelerator_pedal_1(:, 1);

hold on
plot(motor_speed(:,1)/1000,motor_speed(:,2)/100);
plot(S.dc_bus_current(:,1)/1000, S.dc_bus_current(:,2)./4);
plot(commanded_torque(:,1)/1000,commanded_torque(:,2)./10);
plot(requested_torque(:,1)/1000,requested_torque(:,2)./10);
plot(uptime(:,1)/1000,uptime(:,2)/10);
plot(busVoltage(:,1)/1000,busVoltage(:,2)./10);
plot(pedal_time/1000, (pedal_data./100), '.-');

legend({'Motor Speed (RPM)*0.01', ...
    'Current (A)*0.25',...1
    'Commanded Torque*0.1 (Nm)', ...
    'Requested Torque*0.1 (Nm)', ...
    'Uptime (s)', ...
    'DC Voltage(V*0.1)', ...
    'Accel position'})
xlabel('Time (s)')
ylim([-10 100]);
title('Torque, Speed, Current')
h = zoom;
set(h,'Motion','horizontal','Enable','on');



%% Torque, Vehicle Speed, Current
figure

requested_torque = S.requested_torque;
commanded_torque = S.commanded_torque;
feedback_torque = S.torque_feedback;
max_torque=S.max_torque;
busCurrent = S.dc_bus_current;
busVoltage = S.dc_bus_voltage;
motor_speed = S.motor_speed;
vehicle_speed_mph = motor_speed;
vehicle_speed_mph(:,2) = motor_speed(:,2).*0.333.*18.*pi.*60./63360; %%correct mph equation

hold on
plot(motor_speed(:,1)/1000,motor_speed(:,2)./100);
plot(max_torque(:,1)/1000,max_torque(:,2).*.2);
plot(busCurrent(:,1)/1000,busCurrent(:,2)./4);
plot(commanded_torque(:,1)/1000,commanded_torque(:,2)./10);
plot(vehicle_speed_mph(:,1)/1000,vehicle_speed_mph(:,2));
plot(requested_torque(:,1)/1000,requested_torque(:,2)./10);
plot(S.dc_bus_voltage(:,1)/1000,S.dc_bus_voltage(:,2)/4);
legend({'Motor Speed (RPM)*0.01', ...
       'Max Torque (Nm) *.2', ...
       'Current (A)*0.25', ...
       'Commanded Torque*0.1 (Nm)', ...
       'Vehicle Speed (Mph)', ...
       'Requested Torque*0.1 (Nm)', ...
       'DC voltage (v)*0.25'})
xlabel('Time (s)')
title('Torque, Speed, Current')
h = zoom;

set(h,'Motion','horizontal','Enable','on');

%% IDK what this gon be
motor_speed = S.motor_speed;
vehicle_speed_mph = motor_speed;
vehicle_speed_mph(:,2) = motor_speed(:,2).*0.277.*0.000284091.*pi.*60;
figure
hold on
%%plot(S.dc_bus_current(:,1)/1000, S.dc_bus_current(:,2), '.-');
%%plot(S.dc_bus_voltage(:,1)/1000, S.dc_bus_voltage(:,2), '.-'); 
plot(S.dc_bus_current(:,1)/1000, S.dc_bus_current(:,2), '.-');
plot(S.dc_bus_voltage(:,1)/1000, S.dc_bus_voltage(:,2), '.-'); 
plot(S.iq_command(:,1)/1000,S.iq_command(:,2));
plot(S.id_command(:,1)/1000,S.id_command(:,2),'.-');
plot(vehicle_speed_mph(:,1)/1000,vehicle_speed_mph(:,2)*10);
%%plot(S.phase_b_current(:,1)/1000,abs(S.phase_b_current(:,2)));
%%plot(S.phase_c_current(:,1)/1000,abs(S.phase_c_current(:,2)));
%%plot(S.Vd_voltage(:,1)/1000,S.Vd_voltage(:,2),'m');
%%plot(S.Vq_voltage(:,1)/1000,S.Vq_voltage(:,2),'y');
%%plot(S.motor_speed(:,1)/1000,S.motor_speed(:,2)*.1);
%%plot(time, power, '.-');
plot(S.commanded_torque(:,1)/1000,S.commanded_torque(:,2));
plot(S.Iq_Feedback(:,1)/1000,S.Iq_Feedback(:,2));
grid on
xlabel('Time (s)')
ylabel('stuff')
title('stuff')
legend({'DC current','DC voltage','iq command', 'id command','motor_rpm','commanded torque','iq feedback'})
h = zoom;
set(h,'Motion','horizontal','Enable','on');
%% Pedal Input Traces
figure

front_brakes_data = S.brake_transducer_1(:, 2);
front_brakes_time = S.brake_transducer_1(:, 1);

pedal_data = S.accelerator_pedal_1(:, 2);
pedal_time = S.accelerator_pedal_1(:, 1);
% 
% % Normalizing and cleaning pedal traces
% front_brakes_data = front_brakes_data - mode(front_brakes_data);
% front_brakes_data(front_brakes_data < 0) = 0;
% front_brakes_data = front_brakes_data/max(front_brakes_data);
% 
% pedal_data = pedal_data - mode(pedal_data);
% pedal_data(pedal_data < 0) = 0;
% pedal_data = pedal_data/max(pedal_data);

hold on
plot(pedal_time, pedal_data, '.-');
plot(front_brakes_time, front_brakes_data, '.-');
grid on

xlabel('Time (s)')
ylabel('Normalized Pedal Position and Brake Pressure')
title('Brake and Pedal Traces')
legend({'Accelerator Pedal Position','Brake Pressure'})
h = zoom;
set(h,'Motion','horizontal','Enable','on');
%% DC Bus Current, DC Bus Voltage, and Calculated DC Power Output
figure
voltage = S.dc_bus_voltage; 
current = S.dc_bus_current;

% Data uniqueness
for i = 1:length(voltage(:,1)/1000)
    voltage(i,1) = voltage(i,1) + i/100000000;
end
for i = 1:length(current(:,1)/1000)
    current(i,1) = current(i,1) + i/100000000;
end
    
time = 1:0.1:max(current(:,1)/1000); %Seconds
current_adj = interp1(current(:,1)/1000,current(:,2),time);
voltage_adj = interp1(voltage(:,1)/1000,voltage(:,2),time);
power = current_adj.*voltage_adj./1000;
pedal_data = S.accelerator_pedal_1(:, 2);
pedal_time = S.accelerator_pedal_1(:, 1);

hold on
plot(S.dc_bus_current(:,1)/1000, S.dc_bus_current(:,2), '.-');
plot(S.dc_bus_voltage(:,1)/1000, S.dc_bus_voltage(:,2), '.-'); 
plot(S.iq_command(:,1)/1000,S.iq_command(:,2),'-');
plot(S.id_command(:,1)/1000,S.id_command(:,2),'-');
%%plot(S.phase_b_current(:,1)/1000,abs(S.phase_b_current(:,2)));
%%plot(S.phase_c_current(:,1)/1000,abs(S.phase_c_current(:,2)));
%%plot(S.Vd_voltage(:,1)/1000,S.Vd_voltage(:,2),'m');
%%plot(S.Vq_voltage(:,1)/1000,S.Vq_voltage(:,2),'y');

plot(time, power, '.-');
plot(S.commanded_torque(:,1)/1000,S.commanded_torque(:,2)/10);
plot(S.Iq_Feedback(:,1)/1000,S.Iq_Feedback(:,2));
%%plot(S.State(:,1)/1000,S.State(:,2)*50);
%%plot(pedal_time, (pedal_data./10)-93, '.-');
yyaxis right
plot(S.motor_speed(:,1)/1000,S.motor_speed(:,2));
grid on
%%ylim([-10 410]);

xlabel('Time (s)')
ylabel('Voltage (V), Current (A), Power (kW)')
title('DC Bus Current, DC Bus Voltage, and Calculated DC Power Output')
legend({'Current','Voltage', ...
    'Iq Command (A)', ...
    'Id Command (A)',......
    ...'Phase A current','phase b curr','phase c curr', ...
    ...'D-axis V','Q-axis V', ...
    'Power', ...
    'Commanded Torque (Nm)/10','Iq feedback (A)','Motor speed(RPM)/10'})
%%legend({'Current','Voltage','Power'})

h = zoom;
set(h,'Motion','horizontal','Enable','on');
%% Cooling Loop: Motor and MCU Temperatures
figure

hold on
plot(S.gate_driver_board_temperature(:,1)/1000,S.gate_driver_board_temperature(:,2))
plot(S.control_board_temperature(:,1)/1000,S.control_board_temperature(:,2))
plot(S.module_a_temperature(:,1)/1000,S.module_a_temperature(:,2))
plot(S.module_b_temperature(:,1)/1000,S.module_b_temperature(:,2)) 
plot(S.module_c_temperature(:,1)/1000,S.module_c_temperature(:,2))
plot(S.motor_temperature(:,1)/1000,S.motor_temperature(:,2))
plot(S.dc_bus_current(:,1)/1000,S.dc_bus_current(:,2)./10)
plot(S.hightemp(:,1)/1000,S.hightemp(:,2))
plot(S.lowtemp(:,1)/1000,S.lowtemp(:,2))
grid on

legend({'MCU Gate Driver Board Temperature','MCU Control Board Temperature','MCU Module A Temperature','MCU Module B Temperature','MCU Module C Temperature','Motor Temperature','Current/10 (A)','Pack Highest Cell Temp','Pack Lowest Cell Temp'})
xlabel('Time (s)')
ylabel('Temperature (C)')
title('Cooling Loop Temperature Plots')
h = zoom;
set(h,'Motion','horizontal','Enable','on');
%% BMS Acc Voltage Readings vs Inverter Readings and Current
figure
hold on
plot(S.dc_bus_current(:,1)/1000,S.dc_bus_current(:,2))
plot(S.PackCurrent(:,1)/1000,S.PackCurrent(:,2)/10)
plot(S.dc_bus_voltage(:,1)/1000,S.dc_bus_voltage(:,2))
plot(S.PackInstVolt(:,1)/1000,S.PackInstVolt(:,2))
plot(S.PackOpenVolt(:,1)/1000,S.PackOpenVolt(:,2))
plot(S.PackSummedVolt(:,1)/1000,S.PackSummedVolt(:,2))
ylabel('yes')
xlabel('Time (s)')
title('BMS Acc Voltage Readings vs Inverter Readings and Current')
legend('DC Bus Current','Dc Bus Voltage','Instant Voltage','Open Voltage','Summed Voltage')

%% Accumulator Capacity Analysis
current = S.dc_bus_current; %Amps
motorSpeed = S.motor_speed; %RPM
voltage = S.dc_bus_voltage; %Volts
motorSpeed(:,2) = motorSpeed(:,2)./60; %Rotations per second
consumption = cumtrapz(current(:,1),current(:,2));
consumption = [current(:,1),consumption./3600];
distance = cumtrapz(motorSpeed(:,1),motorSpeed(:,2)); %Rotations
distance = [motorSpeed(:,1),(distance./3)*pi*0.4572./1000]; %Kilometers

% Data uniqueness
for i = 1:length(distance(:,1))
    distance(i,1) = distance(i,1) + i/100000000;
end
for i = 1:length(consumption(:,1))
    consumption(i,1) = consumption(i,1) + i/100000000;
end
for i = 1:length(voltage(:,1))
    voltage(i,1) = voltage(i,1) + i/100000000;
end
for i = 1:length(current(:,1))
    current(i,1) = current(i,1) + i/100000000;
end

time = 1:0.1:max(current(:,1)); %Seconds
adjDistance = interp1(distance(:,1),distance(:,2),time);
adjConsumption = interp1(consumption(:,1),consumption(:,2),time);
adjVoltage = interp1(voltage(:,1),voltage(:,2),time);
adjCurrent = interp1(current(:,1),current(:,2),time);
adjPower = adjVoltage.*adjCurrent; %Watts
adjPower(~isfinite(adjPower)) = 0;
adjEnergy = cumtrapz(time(2:end),adjPower(2:end))./3600; %Watt Hours
adjEnergy = adjEnergy./1000; %kWh
% Plotting
figure
subplot(2,1,1)
plot(adjDistance/1000,adjConsumption/1000)
ylabel('Charge (Ah)')
xlabel('Distance Traveled (km)')
title('Accumulator Capacity Usage vs Distance Traveled (No Slip Assumption)')
subplot(2,1,2)
plot(adjDistance(2:end)/1000,adjEnergy/1000)
ylabel('Energy (kWh)')
xlabel('Distance Traveled (km)')
title('Accumulator Energy Expended vs Distance Traveled (No Slip Assumption)')

%% Accumulator Voltage Drop
figure

mask = adjCurrent>10 & adjVoltage>150; %%only use data where current > 10 and voltage >150v
adjCurrent(~mask) = [];
adjVoltage(~mask) = [];

voltageDrop = cat(1, adjCurrent, adjVoltage);
voltageDrop = round(voltageDrop, 2); % Smooth out, only use two decimal places

% Credit: https://www.mathworks.com/matlabcentral/answers/151709-how-can-i-average-points-with-just-the-same-x-coordinate
[uniqueCurrent,~,idx] = unique(voltageDrop(1,:));
averageVoltage = accumarray(idx,voltageDrop(2,:),[],@mean);

plot(uniqueCurrent, averageVoltage,'.-')
xlabel('Current')
ylabel('Voltage')
title('Accumulator Voltage Drop Analysis')

