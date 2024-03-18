%fname=('test_single_1900010100_1900013121.nc');

zmask=zeros(288,192,1);

ndays=[31 28 31 30 31 30 31 31 30 31 30 31];

for year=1950:2023
    for mo=1:12
	    for iday=1:ndays(mo)
            %fname=('test_2layer.nc');
            if mo<10
                fname=(['ERA5regrid/e5.oper.an.pl.128_131_u.regrid.' num2str(year) '0' num2str(mo) 'day' num2str( iday) '.nc']);
                fname2=(['ERA5regrid/e5.oper.an.pl.128_132_v.regrid.' num2str(year) '0' num2str(mo) 'day' num2str( iday) '.nc']);
                fname3=(['ERA5regrid/e5.oper.an.pl.128_130_t.regrid.' num2str(year) '0' num2str(mo) 'day' num2str( iday) '.nc']);
                fname4=(['ERA5regrid/e5.oper.an.pl.128_133_q.regrid.' num2str(year) '0' num2str(mo) 'day' num2str( iday) '.nc']);
            else
                fname=(['ERA5regrid/e5.oper.an.pl.128_131_u.regrid.' num2str(year) '' num2str(mo) 'day' num2str( iday) '.nc']);
                fname2=(['ERA5regrid/e5.oper.an.pl.128_132_v.regrid.' num2str(year) '' num2str(mo) 'day' num2str( iday) '.nc']);
                fname3=(['ERA5regrid/e5.oper.an.pl.128_130_t.regrid.' num2str(year) '' num2str(mo) 'day' num2str( iday) '.nc']);
                fname4=(['ERA5regrid/e5.oper.an.pl.128_133_q.regrid.' num2str(year) '' num2str(mo) 'day' num2str( iday) '.nc']);
            end

            dum=ncread(fname,'u'); %,[1 1 1 1],[inf inf inf inf],[1 1 1 2]); 
            dum2=ncread(fname2,'v'); %,[1 1 1 1],[inf inf inf inf],[1 1 1 2]); 
            dum3=ncread(fname3,'t'); %,[1 1 1 1],[inf inf inf inf],[1 1 1 2]); 
            dum4=ncread(fname4,'q'); %,[1 1 1 1],[inf inf inf inf],[1 1 1 2]); 

            lat=ncread(fname,'lat');
            lon=ncread(fname,'lon');
            lev=ncread(fname,'level');
            time=ncread(fname,'time');

            nyr=year;
            imo=mo;

            hours={'00000','21600','43200','64800'}

            %ERA5.6hour.30level.uvtq.2022-03-07-64800.nc

            is=0;

            %for it=1:size(dum,4)
            for it=1:4
                is=is+1;
                tic
            %    iday=floor((is-1)/4)+1;
    
                hr=mod(is,4);
                if hr==0
                    hr=4;
                end
    
                display(['Day ' num2str(iday)])
                display(['Hour ' char(hours(hr))])
    

                if imo<10
                    if iday<10
                        name_ou=['ERA5_CESM2/ERA5.6hour.32level.uvtq.' num2str(nyr) '-0' num2str(imo) '-0' num2str(iday) '-' char(hours(hr)) '.nc']
                    else
                        name_ou=['ERA5_CESM2/ERA5.6hour.32level.uvtq.' num2str(nyr) '-0' num2str(imo) '-' num2str(iday) '-' char(hours(hr)) '.nc']
                    end
                else
                    if iday<10
                        name_ou=['ERA5_CESM2/ERA5.6hour.32level.uvtq.' num2str(nyr) '-' num2str(imo) '-0' num2str(iday) '-' char(hours(hr)) '.nc']
                    else
                        name_ou=['ERA5_CESM2/ERA5.6hour.32level.uvtq.' num2str(nyr) '-' num2str(imo) '-' num2str(iday) '-' char(hours(hr)) '.nc']
                    end
                end

	            nccreate(name_ou,'U','Dimensions',{'lon',288,'lat',192,'lev',32,'time',1},'Format','classic')
                ncwrite(name_ou,'U',permute(dum(:,:,:,it),[1 2 3 4]))
                ncwriteatt(name_ou,'U','long_name','Zonal wind')
                ncwriteatt(name_ou,'U','units','m/s')

	            nccreate(name_ou,'V','Dimensions',{'lon',288,'lat',192,'lev',32,'time',1},'Format','classic')
                ncwrite(name_ou,'V',permute(dum2(:,:,:,it),[1 2 3 4]))
                ncwriteatt(name_ou,'V','long_name','Meridional wind')
                ncwriteatt(name_ou,'V','units','m/s')

	            nccreate(name_ou,'T','Dimensions',{'lon',288,'lat',192,'lev',32,'time',1},'Format','classic')
                ncwrite(name_ou,'T',permute(dum3(:,:,:,it),[1 2 3 4]))
                ncwriteatt(name_ou,'T','long_name','Temperature')
                ncwriteatt(name_ou,'T','units','K')

	            nccreate(name_ou,'Q','Dimensions',{'lon',288,'lat',192,'lev',32,'time',1},'Format','classic')
                ncwrite(name_ou,'Q',permute(dum4(:,:,:,it),[1 2 3 4]))
                ncwriteatt(name_ou,'Q','long_name','Specific humidity')
                ncwriteatt(name_ou,'Q','units','kg/kg')

                nccreate(name_ou,'PS','Dimensions',{'lon',288,'lat',192,'time',1},'Format','classic')
                ncwrite(name_ou,'PS',zmask)

                nccreate(name_ou,'lat','Dimensions',{'lat',192},'Format','classic') 
                ncwrite(name_ou,'lat',lat)

                nccreate(name_ou,'lon','Dimensions',{'lon',288},'Format','classic')
                ncwrite(name_ou,'lon',lon)

                nccreate(name_ou,'lev','Dimensions',{'lev',32},'Format','classic')
                ncwrite(name_ou,'lev',lev)

                nccreate(name_ou,'time','Dimensions',{'time',1},'Format','classic')
                ncwrite(name_ou,'time',time(it))
                toc
            end
        end
    end
end
