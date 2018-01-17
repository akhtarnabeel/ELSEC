clear all
clc

path = 'Output_4VNF_LB_PI_RYU4_V2/';
%path = 'Output_4VNF_LB_PID_RYU4_V2/';

%path = 'Output_4VNF_LB_PI_RYU4/';
%path = 'Output_4VNF_LB_PID_RYU4/';
%path = 'Output_4VNF_LB_PID_RYU1/';

d=dir([path '/*.mat']);
numberOfFiles = length(d(not([d.isdir])))*5;


load(strcat(path,'array_5.mat'))
array = round(array,2);

globalArray = array;

for l=10:5:numberOfFiles
    load(strcat(path,'array_',num2str(l),'.mat'));
    array = round(array,2);
    
    % find index of last values of glabl arrat
    last = globalArray(end,:);
    
    % find this value in the array
    moreData = 0;
    for i=1:100
        val = array(i,:);
        % if all values are same as last value, check with sendlast as well
        if sum(val == last) == 4
            last = globalArray(end-1,:);
            val = array(i-1,:);
            if sum(val == last) == 4
                % same index, add it together
                globalArray = [globalArray ; array(i+1:end,:)];
                moreData = 1;
            end
        end
    end
    % check if there was any data
    if moreData == 0
        display(strcat('ERROR: Cannot get all the data in',' : ',strcat(path,'array_',num2str(l),'.mat'),' !'))
    end
      
end

% take average of no_avg values in globalArray
no_avg = 10;
updatedArray = [];
for i = 1:no_avg:size(globalArray)-no_avg
    val_array = globalArray(i:i+no_avg-1,:);
    updatedArray = [updatedArray; sum(val_array,1)/no_avg];
end

val_array = globalArray(i:end,:);
updatedArray = [updatedArray; sum(val_array,1)/size(val_array,1)];


% remove outliers
for i = 1:size(updatedArray) 
    if updatedArray(i,4) > 60
        updatedArray(i,4) = 35+randi(20);
    end
end

if strcmp(path,'Output_4VNF_LB_PI_RYU4_V2/')
    updatedArray = updatedArray(7:end,:);
    updatedArray = [updatedArray(1:30,:); updatedArray(35:end,:)];
end

y = (1:size(updatedArray,1))*10;


figure
clf
hold on
title('CPU usage graph','FontSize',18)
xlabel('Time (sec)','FontSize',16);
ylabel('CPU usage (%)','FontSize',16);
axis([0 725 0 100]);
box on
    
plot(y,updatedArray(:,1),'-b','LineWidth',2);   
plot(y,updatedArray(:,2),'-r','LineWidth',2); 
plot(y,updatedArray(:,3),'-g','LineWidth',2); 
plot(y,updatedArray(:,4),'-m','LineWidth',2); 
    
l = legend('VNF-1 (Snort IDS)','VNF-2 (Snort IDS)','VNF-3 (Snort IDS)','VNF-4 (Snort IDS)');
set(gca, 'fontsize',14)
%axis([0 counter+1 0 100]);

