# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BsemembersItem(scrapy.Item):
    data_id = scrapy.Field()
    # website = scrapy.Field()
    company_name = scrapy.Field()
    # email_id = scrapy.Field()
    # registered_office_address = scrapy.Field()
    # company_member_list = scrapy.Field()
    # correspondence_address = scrapy.Field()
    # office_contact_no = scrapy.Field()
    # correspondence_contact_no = scrapy.Field()
    # office_fax = scrapy.Field()
    # correspondence_fax = scrapy.Field()
    # SEBI_Registration_no = scrapy.Field()
    # SEBI_Registration_date = scrapy.Field()
    # Chief_Executive_Name = scrapy.Field()
    # Chief_Executive_Phone = scrapy.Field()
    # Chief_Executive_Email = scrapy.Field()
    Board_Member_Links = scrapy.Field()
    Board_Member_Name = scrapy.Field()
    Board_Member_Email = scrapy.Field()
    Board_Member_Position = scrapy.Field()
    scraped_time = scrapy.Field()
