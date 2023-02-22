import scrapy
import re

class SchoolSpider(scrapy.Spider):
    name = 'school'
    allowed_domains = ['isd110.org']
    start_urls = ['https://isd110.org/our-schools/laketown-elementary/staff-directory']
    
    
    def init_request(self,response):
        
        school_name = response.xpath('//div[@class="paragraph staff default"]//div[@class="field-content"]/span/text()').extract_first().strip()
        address1 = response.xpath('//p[@class="address"]/text()[1]').extract_first().strip()
        address2 = response.xpath('//p[@class="address"]/text()[2]').extract_first().strip()
        address = address1+address2
        state = re.findall(r'[A-Z][A-Z]',address2)[0]
        zip_code =re.findall(r"(?!\A)\b\d{5}(?:-\d{4})?\b",address2)[0]
        names = response.xpath('//div[@class="paragraph staff default"]//h2[@class="title"]/text()').extract()
        job_titles = response.xpath('//div[@class="field job-title"]/text()').extract()
        phones = response.xpath('//div[@class="field phone"]/a/text()').extract()
        emails = response.xpath('//div[@class="field email"]/a/text()').extract()
        
        for name,job_title,phone,email in zip(names,job_titles,phones,emails):
            first_name = name.split(',')[0]
            last_name = name.split(',')[1]
            job_title=job_title.strip()
            yield {
                "School":school_name,
                "Address":address,
                "State":state,
                "Zip":zip_code,
                "First Name":first_name,
                "Last Name":last_name,
                "Title":job_title,
                "Phone":phone,
                "Email":email
            }

    def parse(self, response):
        base_url = 'https://isd110.org/our-schools/laketown-elementary/staff-directory?s=&page='
        pagination = response.xpath('//li[@class="item last"]/a/@href').extract_first()
        len_of_pages = pagination.replace('?s=&page=','')
        
        
        
        for page in range(1,int(len_of_pages)+1):
            
            next_page_url = base_url+str(page)
            yield scrapy.Request(next_page_url,callback=self.init_request)
