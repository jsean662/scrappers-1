class TestListing():
    final_dict = {}

    def checkFurnishing(self, furnishing_list, dict_):
        print 'Running checkFurnishing >>>', furnishing_list
        if furnishing_list:
            self.final_dict['furnishing'] = furnishing_list
        else:
            self.final_dict['furnishing'] = 'None'

    def checkTt(self, tt_list, dict_):
        print 'Running checkTt >>>', tt_list
        if tt_list:
            self.final_dict['tt'] = tt_list[0]
        else:
            self.final_dict['tt'] = 'None'

    def checkPt(self, pt_list, dict_):
        print 'Running checkPt >>>', pt_list
        if pt_list:
            self.final_dict['property_type'] = pt_list[0]
        elif 'BHK' in dict_['config'] or 'bhk' in dict_['config']:
            self.final_dict['property_type'] = 'Home'
        else:
            self.final_dict['property_type'] = 'None'

    def checkDeal(self, deal_list, dict_):
        print 'Running checkDeal >>>', deal_list
        if deal_list:
            self.final_dict['req_avl'] = deal_list[0]
        else:
            self.final_dict['req_avl'] = 'test'

    def checkConfig(self, config_list, dict_):
        print 'Running checkConfig >>>', config_list
        if len(config_list) == 1:
            self.final_dict['config'] = config_list[0]
        if len(config_list) > 1:
            self.final_dict['config'] = config_list[0]
        # set default as 2 bhk if config list empty
        if not config_list:
            self.find_config['config'] = 'None'

    def getPrice(self, price):
        print price

    def checkPrice(self, price_dict, dict_):
        print 'Running checkPrice >>>', price_dict
        p_key = price_dict.keys()

        if 'composite_price' in p_key:
            if price_dict['composite_price']:
                for prc in price_dict['composite_price']:
                    try:
                        price_dict['price'] += [prc['price']]
                        price_dict['label_amt_units'] += [prc['label_amt_units']]
                    except:
                        price_dict['price'] = [prc['price']]
                        price_dict['label_amt_units'] = [prc['label_amt_units']]

        p_key = price_dict.keys()
        if 'label_amt_units' in p_key:
            if price_dict['label_amt_units']:
                for n, elemnt in enumerate(price_dict['label_amt_units']):
                    if 'k' in elemnt or 'pkg' in elemnt:
                        price_dict['label_amt_units'][n] = 1000
                    if 'lac' in elemnt:
                        price_dict['label_amt_units'][n] = 100000
                    if 'cr' in elemnt:
                        price_dict['label_amt_units'][n] = 10000000
                if len(price_dict['label_amt_units']) == 1:
                    price_dict['label_amt_units'] += [1]

        if 'price' in p_key and len(price_dict['price']) <= 2:
            p_list = []
            if price_dict['price']:
                if ('label_amt_units' in price_dict.keys()) and price_dict['label_amt_units']:
                    if len(price_dict['price']) == 1:
                        price_dict['price'] += [1]
                    for r_elmnt in price_dict['price']:
                        if len(price_dict['label_amt_units']) >= 1:
                            for c_elmnt in price_dict['label_amt_units']:
                                p_list.append(int(r_elmnt*c_elmnt))
                        else:
                            p_list.append(int(r_elmnt))
                else:
                    p_list = price_dict['price']
            print 'After label to price >>>', price_dict
            print 'all price figures >>>', p_list
            fmtd_price = []

            if not fmtd_price:
                # for one value in price and label
                for dr in p_list:
                    if [nr/dr for nr in p_list] == [1, 0, 0, 0]:
                        fmtd_price = [(p_list[0], 0)]
                        print fmtd_price

            if not fmtd_price:
                # for Range case
                c = 0
                for dr in p_list:
                    if [nr/dr for nr in p_list] in [[1, 1, 1, 1], [0, 0, 1, 1]]:
                        c += 1
                    if c > 3:
                        fmtd_price = [((p_list[1]+p_list[2])/2, 0)]
                        print fmtd_price

            if not fmtd_price:
                # for two price and one label
                for dr in p_list:
                    if [nr/dr for nr in p_list] == [1, 0, 1, 0]:
                        fmtd_price = [((p_list[0]+p_list[2])/2, 0)]
                        print fmtd_price

            if not fmtd_price:
                # for rental+deposite case
                if 'LL' in dict_['tt'] or 'L/L' in dict_['tt']:
                    fmtd_price = [(dr, nr) for dr in p_list
                                  for nr in p_list if nr/dr >= 2 and nr/dr <= 10]
                    print fmtd_price

            if not fmtd_price:
                # only habing price not label
                fmtd_price = [(p_list[0], 0)]
                print fmtd_price

        if 'LL' in dict_['tt']:
            self.final_dict['price'] = fmtd_price[0][0]
            if fmtd_price[0][1] == 0:
                self.final_dict['deposit'] = fmtd_price[0][0]*3
            else:
                self.final_dict['deposit'] = fmtd_price[0][1]

        if 'OR' in dict_['tt']:
            self.final_dict['price'] = fmtd_price[0][0]
            self.final_dict['deposit'] = 0

    def checkArea(self, area_dict):
        print area_dict

    def checkLocality(self, loc_list, dict_):
        print 'Running checkLoc >>>', loc_list
        if loc_list:
            self.final_dict['locality'] = loc_list
        else:
            self.final_dict['locality'] = ['None']

    def checkPark(self, park_dict, dict_):
        print 'Running checkPark >>>', park_dict
        if 'no' in park_dict.keys():
            if park_dict['no']:
                self.final_dict['parking'] = park_dict['no'][0]

    def checkListing(self, make_dict_chk):
        self.final_dict = {}
        print "Running checkList >>>"
        price_keys = ['label_amt_units', 'composite_price', 'label_deposit', 'price',
                      'label_currency_Rs']
        # area_keys = ['composite_area', 'label_area', 'label_area_units', 'sqft']
        park_keys = ['composite_parking', 'label_park', 'no']

        try:
            self.final_dict['Actual_msg'] = make_dict_chk['Actual_msg']
        except:
            print 'No actual mesg'
        self.final_dict['phonenumber'] = make_dict_chk['phone_number'][0]
        self.final_dict['listing_date'] = make_dict_chk['listing_date'][0]
        try:
            self.checkDeal(make_dict_chk['req_avail'], self.final_dict)
        except:
            self.checkDeal(['Default'], self.final_dict)
        try:
            self.checkConfig(make_dict_chk['config'], self.final_dict)
        except:
            self.checkConfig(['None'], self.final_dict)
        print self.final_dict
        try:
            self.checkTt(make_dict_chk['transaction_type'], self.final_dict)
        except:
            self.checkTt(['None'], self.final_dict)
        print self.final_dict
        try:
            self.checkPt(make_dict_chk['property_type'], self.final_dict)
        except KeyError:
            self.checkPt([], self.final_dict)
        print self.final_dict
        try:
            self.checkPrice({key: make_dict_chk[key]
                            for key in price_keys if key in make_dict_chk.keys()},
                            self.final_dict)
        except:
            self.checkPrice({'price': [1]}, self.final_dict)
        print self.final_dict
        # self.checkArea({key: make_dict_chk[key]
        #                 for key in area_keys if key in make_dict_chk.keys()},
        #                self.final_dict)
        try:
            self.checkLocality(make_dict_chk['label_locality_mum'], self.final_dict)
        except:
            self.checkLocality([], self.final_dict)
        print self.final_dict
        try:
            self.checkFurnishing(make_dict_chk['furnishing'], self.final_dict)
        except:
            self.checkFurnishing([], self.final_dict)
        print self.final_dict
        self.checkPark({key: make_dict_chk[key]
                        for key in park_keys if key in make_dict_chk.keys()},
                       self.final_dict)
        print "\nAfter Preparing final dict >>>"
        print self.final_dict
        return self.final_dict
