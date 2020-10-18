import requests
from bs4 import BeautifulSoup
import time
from common.constant import Mysql,Http_Head
from common.database import Database
from common.log import print_log
from common.random_ip import random_ip
import os
import random
from common.get_sql import get_insert_sql_ip,get_update_sql_ip

class IpPool(Database):

    def __init__(self,database):
        self.database =database

        super().__init__(self.database)
    def get_data(self):
        url = "https://ip.ihuan.me/"
        proxies=random_ip(self.select_all_date())
        try:
            page = requests.get(url, headers=Http_Head.headers,proxies=random.choice(proxies))
            soup = BeautifulSoup(page.text, "html.parser")
            soups = soup.find("tbody").find_all("tr")
            ip_list = []
            for soup in soups:
                ip_dict = {}
                ip_dict["ip"] = soup.find_all("td")[0].text
                ip_dict["port"] = soup.find_all("td")[1].text
                ip_list.append(ip_dict)
                self.stats_dict["get_ip"][1]+=1
            return ip_list
        except Exception as e:
            print_log("error", "Wrong with %s" % str(e))
            self.stats_dict["get_ip"][2] += 1
            self.get_data()


    def insert_data(self):
        self.stats_dict["get_ip"][0] += 1
        if self.row_number < 109:
            print_log("info", "Get ip start")
            ip_list = self.get_data()
            result = {}
            for i in range(len(ip_list)):
                result["id"] = i + self.row_number
                result["ip"] = ip_list[i]["ip"]
                result["port"] = ip_list[i]["port"]
                result["update_time"] = int(time.time())
                result["status"] = 1
                sql = get_insert_sql_ip(result)
                try:
                    self.cursor.execute(sql)
                    self.database_use.commit()
                    print_log("info", "IP %s has gotten" % str(result["ip"]))
                except Exception as e:
                    print_log("error", "%s" % str(e))
        else:
            print_log("info", "Update ip start")
            self.update_data()
            print_log("info", "Update ip end")
        self.close_file()
    def update_data(self):
        self.stats_dict["update_ip"][0] += 1
        if (self.cursor.execute("select * from ippool where status='0'") > 0):
            rows = self.cursor.fetchall()
            ip_list = self.get_data()
            result = {}
            for row in rows:
                for ip in ip_list:
                    if ip["ip"] != row[0]:
                        result["id"] = row[4]
                        result["ip"] = ip["ip"]
                        result["port"] = ip["port"]
                        result["update_time"] = int(time.time())
                        result["status"] = 1

                        sql = get_update_sql_ip(result)
                        try:
                            self.stats_dict["update_ip"][1] += 1
                            self.cursor.execute(sql)
                            self.database_use.commit()
                            print_log("info", "IP %s has updated" % str(result["ip"]))
                        except Exception as e:
                            self.stats_dict["update_ip"][2] += 1
                            print_log("error", "%s" % str(e))
        else:
            print_log("info", "No IP need to update")

    def check_ip(self):
        self.stats_dict["check_ip"][0] += 1
        print_log("info", "IP check start")
        select_all_sql = "select id, ip from %s" % Mysql.IPPOOL
        self.cursor.execute(select_all_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            result = os.system("ping %s -w 5" % str(row[1])) == 0
            if (result == True):
                self.stats_dict["check_ip"][1] += 1
                self.cursor.execute("update ippool set status=1 where id='%s'" % row[0])
                print_log("info", "IP %s is working " % str(row[1]))
            else:
                self.stats_dict["check_ip"][2] += 1
                self.cursor.execute("update ippool set status=0 where id='%s'" % row[0])
                self.database_use.commit()
                print_log("warning", "ip %s has no effect" % str(row[1]))
        print_log("info", "IP check end")
        self.close_file()


