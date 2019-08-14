import pprint

def model_statistics(portefolio, dataset):

    data = dataset.__all__()
    value = portefolio.get_value(data)

    print('{0:40} \t {1} \t {2:10} \t {3:10} \t {4} \t {5} \t {6}'.format('name', 'amount', 'purchase price', 'current price', 'purchase ratio %', 'current ratio %', 'change %'))
    for stock in portefolio.deposit:
        original_part = round(portefolio.deposit[stock][0] * portefolio.deposit[stock][1] / portefolio.start_cap * 100, 2)
        current_part = round(portefolio.deposit[stock][0] * data[stock]['Close Price'][0] / value * 100, 2)

        print('{0:40} \t {1} \t {2:10} \t {3:10} \t {4} \t {5} \t {6}'.format(stock,
                                                             portefolio.deposit[stock][0],
                                                             portefolio.deposit[stock][1],
                                                             data[stock]['Close Price'][0],
                                                             original_part,
                                                             current_part,
                                                             round(data[stock]['Close Price'][0] / portefolio.deposit[stock][1] * 100 - 100,2)))

    print()
    print("Value ", round(value,2))
    print("Procent return ", round((value / portefolio.start_cap)*100 - 100,2))
    print()