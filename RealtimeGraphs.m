clear all
clc

% controller name
controllerNode = 'nabeel@pcvm2-15.instageni.gpolab.bbn.com';

% save figures and values
saveFigures = true;

% path to files
path = '~/Control/RINA';

path = strtrim(path);

% remove local text files
system('rm *.txt');

commandToFile = strcat('scp',{' '},controllerNode,':',path,'/NFV* .');
commandToFile = commandToFile{1};

fileNameNFV1 = 'NFV1.txt';
fileNameNFV2 = 'NFV2.txt';
fileNameNFV3 = 'NFV3.txt';
fileNameNFV4 = 'NFV4.txt';

figure

c = 0;

%% Following code is just to make sure that we only update when there is change is the measurement file

%check if the file exists, if no, then change the figure and wait file
while(true)
    ANS = system(commandToFile);
    if ANS ~= 1
    	break; 
    end
    pause(10);
end

cpu1_old = fileread(fileNameNFV1);
cpu2_old = fileread(fileNameNFV2);
cpu3_old = fileread(fileNameNFV3);
cpu4_old = fileread(fileNameNFV4);

%% END


while (true)

    pause(10);

    %check if the file exists, if no, then change the figure and wait file
    while(true)
        ANS = system(commandToFile);
        if ANS ~= 1
            break; 
        end
        pause(0.2);
    end
    
    %% Following code is just to make sure that we only update when there is change is the measurement file
    
    cpu1 = fileread(fileNameNFV1);
    cpu2 = fileread(fileNameNFV2);
    cpu3 = fileread(fileNameNFV3);
    cpu4 = fileread(fileNameNFV4);
    
    if ((size(cpu1,2) == size(cpu1_old,2)) && (size(cpu2,2) == size(cpu2_old,2)) && (size(cpu3,2) == size(cpu3_old,2)) && (size(cpu4,2) == size(cpu4_old,2)) )
        if sum(cpu1 ~= cpu1_old)==0 || sum(cpu2 ~= cpu2_old)==0 || sum(cpu3 ~= cpu3_old)==0 || sum(cpu4 ~= cpu4_old)==0
            continue;
        end
    end
    %% END
    
    cpu1_old = cpu1;
    cpu2_old = cpu2;
    cpu3_old = cpu3;
    cpu4_old = cpu4;
    
    fin1=fopen(fileNameNFV1,'r');
    fin2=fopen(fileNameNFV2,'r');
    fin3=fopen(fileNameNFV3,'r');
    fin4=fopen(fileNameNFV4,'r');

    array = zeros(10000,4);
    
    counter = 0;
    
    while ~feof(fin1)
       
       txt1=fgets(fin1); 
       txt2=fgets(fin2); 
       txt3=fgets(fin3); 
       txt4=fgets(fin4); 
       
       % sometimes error in the file
       if isnumeric(txt1) || isnumeric(txt2) || isnumeric(txt3) || isnumeric(txt4)
           continue
       end
       
       dataCPU1 = strsplit(txt1,'=');
       dataCPU2 = strsplit(txt2,'=');
       dataCPU3 = strsplit(txt3,'=');
       dataCPU4 = strsplit(txt4,'=');
       
       cpuUsuage1 = str2num(dataCPU1{2});
       cpuUsuage2 = str2num(dataCPU2{2});
       cpuUsuage3 = str2num(dataCPU3{2});
       cpuUsuage4 = str2num(dataCPU4{2});
       
       counter = counter+1;
       array(counter,1) = cpuUsuage1;
       array(counter,2) = cpuUsuage2;
       array(counter,3) = cpuUsuage3;
       array(counter,4) = cpuUsuage4;
      
    end

    array = array((1:counter),:);
    
    y = (1:counter);
    
    clf
    hold on
    title('CPU usage graph','FontSize',18)
    xlabel('Time','FontSize',16);
    ylabel('CPU usage','FontSize',16);
    axis([0 counter+1 0 100]);
    box on
    
    plot(y,array(:,1),'-b','LineWidth',2);   
    plot(y,array(:,2),'-r','LineWidth',2); 
    plot(y,array(:,3),'-g','LineWidth',2); 
    plot(y,array(:,4),'-m','LineWidth',2); 
    
    l = legend('SNORT-IDS-1','SNORT-IDS-2','SNORT-IDS-3','SNORT-IDS-4');
    set(gca, 'fontsize',14)
    axis([0 counter+1 0 100]);
    
    pause(0.2);
    
    fclose(fin1);
    fclose(fin2);
    fclose(fin3);
    fclose(fin4);
    
    c=c+1;
    
    if saveFigures == true
        if mod(c,5)==0
            % Save figure for future use
            fpat='Output';
            fnam=strcat('foo_',num2str(c),'.fig');
            saveas(gcf,[fpat,filesep,fnam],'fig');
            % save variable
            varName = strcat('Output/array_',num2str(c),'.mat');
            save(varName, 'array')
        end
    end
    %}
    
end
