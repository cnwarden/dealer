#coding:utf-8

import urllib2
import json
from BeautifulSoup import BeautifulSoup
import re as regex
from tidylib import tidy_document
import threading
import time

class SinaDS(object):
    def __init__(self):
        self.trade_records = []
        self.mutex = threading.Lock()
    
    def __format_json(self, data):
        p = regex.compile(r'\\(?![/u"])')
        fixed = p.sub(r"\\\\", data)
        return fixed
    
    def __format_json_stock(self, data):
        p = regex.compile(r',(\w)')
        fixed = p.sub(r',"\1', data)
        p1 = regex.compile(r',"(\w*?):')
        fixed1 = p1.sub(r',"\1":', fixed)
        p2 = regex.compile(r'symbol')
        fixed2 = p2.sub(r'"symbol"', fixed1)
        return fixed2

    def get_reference(self):
        ''' record format: instrument id and name tuple '''
        response = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes')
        data = response.read().decode('GB2312')
        jsonObj = json.loads(self.__format_json(data))
        
        #沪市A股 代码sh_a
        stock_code = jsonObj[1][0][1][4][1][0][2]
        
        re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=%s' % (stock_code))
        data = re.read().decode('GB2312')
        m = regex.search("\"(.*)\"", data)
        numOfItems = 0
        if m:
            numOfItems = int(m.group(1))

        #Get all items in one page
        re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%d&sort=symbol&asc=1&node=%s&symbol=&_s_r_a=init' % (numOfItems, stock_code))
        data = re.read().decode('GB2312')

        stockObjs = json.loads(self.__format_json_stock(data))
        try:
            if stockObjs:
                for stock in stockObjs:
                    yield (stock["code"], stock["name"])
        except Exception,e:
            print e
    
    def __trading_years(self, instrument):
        re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml' % (instrument))
        document, errors = tidy_document(re.read())
        soup = BeautifulSoup(document)
        node = soup.find('select', attrs={'name':'year'})
        for option in node.findAll('option'):
            yield option.getText()

    def __run_threads(self, threads):
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        del threads[:]

    def __worker(self, url):
        print url
        re = urllib2.urlopen(url, None, 5)
        document, errors = tidy_document(re.read())
        soup = BeautifulSoup(document)
        try:
            node = soup.find('tr', attrs={'class':'tr_2'})
            nodes = node.fetchNextSiblings()
            for node in nodes:
                trade_record = []
                for field in node.findAll('div'):
                    trade_record.append(field.getText())
                    
                self.mutex.acquire()
                self.trade_records.append(trade_record)
                self.mutex.release()
        except Exception:
            #parse error, ignore
            pass
            
    def get_trade_history(self, instrument):
        threads = []
        urls = self.get_trade_history_urls(instrument)
        for i, url in enumerate(urls):
            print '[%d/%d]' % (i, len(urls))
            threads.append(threading.Thread(target=self.__worker, args=[url,]))
            if (i+1)%10==0:
                self.__run_threads(threads)
        self.__run_threads(threads)

        return self.trade_records

    def get_trade_history_urls(self, instrument):
        ''' record format: date,open,high,close,low,volume,turnover '''
        urls = []
        for year in self.__trading_years(instrument):
            for season in (4,3,2,1):
                urls.append('http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%s&jidu=%d' % (instrument, year, season))
        return urls
        
    def export(self, trade_iterator):
        for record in trade_iterator:
            print ','.join(record)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    