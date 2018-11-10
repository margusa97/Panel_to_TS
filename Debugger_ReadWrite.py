#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 07:26:35 2018

@author: Marco
"""
import numpy as np
import pandas as pd
import ReadWrite

def transform(x):
    return str(x.date())

def debugging_single_stock(file, stock, mrkt, item):
    rd = ReadWrite(file, stock)
    directory = '/Users/Marco/Desktop/INTERNSHIP IGIER/RAW DATA/Raw_Data_Marco'
    s = 0
    if s ==0:
        dates = list(map(transform, rd.df.columns[1::11]))
    ncol = rd.df.shape[1]


#--------------------------------------------------------------------------


            #BUILDING THE FIRST BLOCK
            
    if rd.check_presence(0, mrkt) == True:
        initial_block, grid = rd.build_first_block(mrkt, dates, 0)
        dict_markets_range = rd.create_dictionary(initial_block)
        primary_markets = np.unique(initial_block[:,2:][:,0])[1:]
        disgr =  np.unique(initial_block[:,3:][:,0])[1:]
        c = 0
        j = 0
        
        
    else: 
        k = 0
        j = 0
        while True:
            if sum(pd.notna(rd.df[rd.df.columns[k]])) == 0:
                k += 11
                j += 1 
                continue
            if rd.check_presence(k, mrkt) == True:
                break
            k += 11
            j += 1
        c = k 
        initial_block, grid = rd.build_first_block(mrkt, dates, c)
        print('INITIAL BLOCK')
        print(initial_block)
        print()
        dict_markets_range = rd.create_dictionary(initial_block)
        primary_markets = np.unique(initial_block[:,2:][:,0])[1:]
        print('PRIMARY MARKETS')
        print(primary_markets)
        print()
        disgr =  np.unique(initial_block[:,3:][:,0])[1:]
        print('TRADES')
        print(disgr)
        print()
            
            
    while c < ncol:
#                print(str(rd.df.columns[c + 1].date()))
#                print()
        if sum(pd.notna(rd.df[rd.df.columns[c]])) == 0:
            c += 11
            j += 1
            continue
        if rd.check_presence( c, mrkt) == False:
            c += 11
            j += 1
            continue 
#---------------------------------------------------------------------------
                #GETTING NAMES, ROWS AND TRADES
        names = rd.get_rows(c,mrkt)[1].tolist()
        rws = rd.get_rows(c, mrkt)[0].tolist()
        trades = rd.get_rows(c, mrkt)[3]
#---------------------------------------------------------------------------
        
        bound_3 = rd.get_rows(c, mrkt)[2]
        rws.append(bound_3)
        aux_dic = dict(zip(rd.get_rows(c, mrkt)[1].tolist(), rd.get_rows(c, mrkt)[0].tolist()))
                            
#---------------------------------------------------------------------------#NEW PRIMARY MARKEY
        if len(np.setdiff1d(names, primary_markets)) > 0:
            print('NEW MARKET')
            print()
            news = np.setdiff1d(names, primary_markets).tolist()
            initial_block, grid = rd.add_new_prim_market(c, news, initial_block, mrkt, primary_markets, dict_markets_range, grid, dates)
            primary_markets = np.unique(initial_block[:,2:][:,0])[1:]
            dict_markets_range = rd.create_dictionary(initial_block)
            disgr =  np.unique(initial_block[:,3:][:,0])[1:]
        
#--------------------------------------------------------------------------
#NEW TRADE
        if len(np.setdiff1d(trades, disgr)) > 0:
            print('NEW TRADE')
            print()
            news = np.setdiff1d(trades, disgr).tolist()
            initial_block, grid = rd.add_trade(news,  initial_block, mrkt, grid, dates)
            dict_markets_range = rd.create_dictionary(initial_block)
            disgr =  np.unique(initial_block[:,3:][:,0])[1:]
            primary_markets = np.unique(initial_block[:,2:][:,0])[1:]
#--------------------------------------------------------------------------
#GETTING AND COPYING THE VALUES
        vals = rd.get_range_values(c, item, mrkt).values
        if '�' in vals:
            ind = np.argwhere( vals == '�')
            vals[ind] = 0
        if '∞' in vals: 
            ind = np.argwhere( vals == '∞')
            vals[ind] = 0
            print('Values')
            print(vals)
            print()
        grid = rd.put_values(dict_markets_range, aux_dic, grid, names, vals, j)
#---------------------------------------------------------------------------
        c += 11
        j += 1
    grid = np.hstack((initial_block, grid))
    final_df = pd.DataFrame(data = grid)
    dates.insert(0, 'Trade')
    dates.insert(0, 'Primary Markets')
    dates.insert(0, 'Market')
    dates.insert(0, 'Stock')
    final_df.rename(columns = dict(zip(final_df.columns, dates)), inplace = True )
    writer = pd.ExcelWriter(directory +'/'+mrkt+'_'+ item +'.xlsx')
    final_df.to_excel(writer,'Sheet1')
    writer.save()