Comment out from sanic_main.py
    # Failed attempt, employ query outside instead
    #def getDaily(self,name,st_dt):
        #return (Mins
               #.select()
               #.where(
                   #(stock==name)
                   #&(dt > st_dt)
                   #&(dt < datetime.now())
               #).limit(6))


#generate_crud(app, [Mins])
now_dt = get_hq_dt("now")
name = "sz300474"
hq_st_dt = get_hq_dt("start")
minhq = Mins.select().where((Mins.stock == name)
                            & (Mins.dt > hq_st_dt))  # .limit
#lsthq = minhq.where(Mins.dt > hq_st_dt)
lsthq = []
# for it in minhq:
#print("Details ==> {}\n @time ==> {}".format(it.detail,it.dt))
#lsthq.append([it.detail, it.dt])

# Jsonfy,versus  text response , had different format, don't figure out Y


    # _date = datetime.strptime(sdate,"%Y%m%d") print("namedate splite {} == {}".format(name,sdate))
