# # SPARQL forespørgsel der returnerer wikidata emner for SMK der ikke har et billede og er markeret som public domain

# SELECT DISTINCT ?item ?billeder ?skaber ?inventarnummer ?commonscat ?English ?ophavsretsstatus WHERE {
#   ?item wdt:P195 wd:Q671384. # emner fra SMK
#   FILTER((LANG(?English)) = "en") # vis kun engelske labels
#   FILTER(NOT EXISTS { ?item wdt:P18 ?billeder. }) # vis kun emner uden billeder
#   FILTER(?ophavsretsstatus = wd:Q19652) # vis kun emner markeret som public domain
#   OPTIONAL { ?item wdt:P217 ?inventarnummer. } # vis inventarnummer
#   OPTIONAL { ?item wdt:P170 ?skaber. } # vis skaber
#   OPTIONAL { ?item wdt:P18 ?billeder. } # vis billeder
#   OPTIONAL { ?item wdt:P373 ?commonscat. } # vis wikimedia commons kategori
#   OPTIONAL { ?item wdt:P1476 ?English. } # vis label
#   OPTIONAL { ?item wdt:P6216 ?ophavsretsstatus. } # vis ophavsretsstatus
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
# }
# ORDER BY (?item)

