from collect_sale_links.collect_links import perform_google_search, filter_links


item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
# item_name = 'Armasight BNVD-51 Gen 3 Pinnacle Night Vision Goggle'


def main():
    # unfiltered_link_list = perform_google_search(item_name)
    # if not unfiltered_link_list:
    #     print(f'No search results found for "{item_name}"')
    #     return
    
    # for url in unfiltered_link_list:
    #     print(url)
    # print(f'Total search results: {len(unfiltered_link_list)}')

    # with open('./printout_data/unfiltered_links.txt', 'w') as f:
    #     for url in unfiltered_link_list:
    #         f.write(url + '\n')

    with open('./printout_data/unfiltered_links.txt', 'r') as f:
        unfiltered_link_list = f.read().splitlines()

    competitor_link_list = filter_links(unfiltered_link_list, item_name)
    if not competitor_link_list:
        print('No competitors found')
        return
    for url in competitor_link_list:
        print(url)  

    print(f'Total competitors: {len(competitor_link_list)}')
    



if __name__ == "__main__":
    main()