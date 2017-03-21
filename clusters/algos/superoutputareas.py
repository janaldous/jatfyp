import sparql
import pandas as pd
import outputareas as oa

#https://pypi.python.org/pypi/sparql-client

def get_super_output_areas_middle():
    endpoint = "http://statistics.data.gov.uk/sparql"

    s = sparql.Service(endpoint, "utf-8", "GET")

    statement = """PREFIX sg: <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX se: <http://statistics.data.gov.uk/def/statistical-entity#>

    SELECT *
    WHERE {
      ?s sg:officialname ?l.
      FILTER regex(?l, "Lambeth", "i").
      ?s se:code <http://statistics.data.gov.uk/id/statistical-entity/E02>
    }

    LIMIT 100"""

    result = s.query(statement)

    codes = []

    for row in result.fetchall():
        code = row[0].__str__()
        codes.append(code[-9:])

    return codes

def convert_oa_to_soasm(oa):
    endpoint = "http://statistics.data.gov.uk/sparql"

    s = sparql.Service(endpoint, "utf-8", "GET")

    statement = """PREFIX sg: <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX se: <http://statistics.data.gov.uk/def/statistical-entity#>

    SELECT *
    WHERE {
      <http://statistics.data.gov.uk/id/statistical-geography/"""+ oa +"""> sg:parentcode ?p.
      ?p sg:parentcode ?pp
    }

    LIMIT 5"""

    result = s.query(statement)

    output = ""
    for row in result.fetchone():
        output = row

    code1 = output[0].__str__()[-9:]
    code2 = output[1].__str__()[-9:]

    return (code1, code2)

def get_soa_ml_list():
    df = pd.read_csv('../spss.csv')
    df['SOA_ML'] = 0
    df['SOA_LL'] = 0
    oas = oa.get_output_areas_from_spss()
    for area in oas:
        soa = convert_oa_to_soasm(area)
        df.loc[df.OA11 == area, ['SOA_LL', 'SOA_ML']] = soa[0], soa[1]
            #print ("%s, %s, %s" % (area, soasm[0], soasm[1]))
        #print d
    print df.SOA_ML.value_counts()
    df.to_csv('newspss.csv')

#E00015671, E01003109, E02000620
def label_soas_ml(row):
   if row['OA11'] == 1 :
      return 'Hispanic'
   return 'Other'
