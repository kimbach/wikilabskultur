from datetime import datetime
from typing import List, Any, TypeVar, Callable, Type, cast
import dateutil.parser
import wikidata

class quickstatement:
    id: str
    retrieved_date: datetime
    inception_date: datetime
    modified_date: datetime
    wikidata_item: str
    publisher: str
    ref_url: str

    def __init__(self, id,retrieved_date, inception_date, modified_date, wikidata_item, publisher, ref_url) -> None:
        self.id = id
        self.retrieved_date = retrieved_date
        self.inception_date = inception_date
        self.modified_date = modified_date
        self.wikidata_item = wikidata_item
        self.publisher = publisher
        self.ref_url = ref_url


    def reference_url(self,as_source=True,url=None):
        # Use default reference_url or specific one passed as url parameter
        if url==None:
            ref_url=self.ref_url
        else:
            ref_url=url

        if not as_source:
            # Generate QS statement
            qs=self.prefix()+'\t'
            qs=qs+wikidata.wd_reference_url.replace('S', 'P') + '\t'
            qs=qs+'"' + ref_url + '"\t'
        else:
            qs=''

        qs=qs+wikidata.wd_reference_url+'\t"' + ref_url + '"' + \
            '\t'+wikidata.wd_inception+'\t' + self.date(self.inception_date, 11) + \
            '\t'+wikidata.wd_retrived+'\t' + self.date(self.retrieved_date,11) + \
            '\t'+wikidata.wd_last_update+'\t' + self.date(self.modified_date,11) + \
            '\t'+wikidata.wd_publisher+'\t'+self.publisher+ \
            '\t'+wikidata.wd_inventory_number+'\t' + '"' + self.id + '"' 
        return qs

    def prefix(self):
        if self.wikidata_item=="":
            qs='LAST'
        else:
            qs=self.wikidata_item
        return qs

    def date(self,date,precision=9):
        # The precision is:
        # 0 - billion years
        # 1 - hundred million years
        # 6 - millennium
        # 7 - century
        # 8 - decade
        # 9 - year (default)
        # 10 - month
        # 11 - day
        return date.strftime("+%Y-%m-%dT%H:%M:%SZ/" + str(precision))
    
    def label(self,label_txt,language):
        qs=''
        qs=qs+self.prefix()+'\tL'+ language + '\t"'+label_txt+ '"'
        return qs

    def description(self,desc_txt,language):
        qs=''
        qs=qs+self.prefix()+'\tD'+ language + '\t"'+desc_txt+ '"'
        return qs

    def comment(self,comment_txt):
        qs=''
        qs=qs+' /* ' + comment_txt + ' */'
        return qs

    def has_works_in_collection(self,url=None):
        qs=self.prefix()+'\t'+wikidata.wd_has_works_in_collection + \
            '\t' + self.publisher + \
            '\t'+self.reference_url(url=url)
        return qs

    def gender(self,gender_txt):
        qs=self.prefix()+'\t'+wikidata.wd_gender_or_sex + \
            '\t' + gender_txt + \
            '\t'+self.reference_url()
        return qs

    def nationality(self,nationality_txt):
        qs=self.prefix()+'\t'+wikidata.wd_country_of_citizenship + \
            '\t' + '"' + nationality_txt + '"' + \
            '\t'+self.reference_url()
        return qs

    def date_of_birth(self,dob,dob_end,precision):
        qs=self.prefix()+'\t'+wikidata.wd_date_of_birth + \
            '\t' + self.date(dob,precision)
        
        if dob_end!=None:
            if dob!=dob_end:
                qs=qs+'\t'+wikidata.wb_lastest_date+'\t'+self.date(dob_end,precision)

        qs=qs+'\t'+self.reference_url()

        return qs

    def date_of_death(self,dod,dod_end,precision):
        qs=self.prefix()+'\t'+wikidata.wd_date_of_death + \
            '\t' + self.date(dod,precision)
        if dod_end!=None:
            if dod!=dod_end:
                qs=qs+'\t'+wikidata.wb_lastest_date+'\t'+self.date(dod_end,precision)

        qs=qs+'\t'+self.reference_url()
        return qs

    def occupation(self,occupation_item=wikidata.wd_artist):
        qs=self.prefix()+'\t'+wikidata.wd_occupation + \
            '\t' + occupation_item + \
            '\t'+self.reference_url()
        return qs

    def instance_of(self,instance_item=wikidata.wb_human):
        qs=self.prefix()+'\t'+wikidata.wd_instance_of + \
            '\t' + instance_item + \
            '\t'+self.reference_url()
        return qs

def test():
    print('')

