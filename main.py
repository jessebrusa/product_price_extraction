from collect_sale_links.collect_links import perform_google_search, filter_links


item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
# item_name = 'Armasight BNVD-51 Gen 3 Pinnacle Night Vision Goggle'


def main():
    unfiltered_link_list = perform_google_search(item_name)
    if not unfiltered_link_list:
        print(f'No search results found for "{item_name}"')
        return

    competitor_link_list = filter_links(unfiltered_link_list, item_name)
    if not competitor_link_list:
        print('No competitors found')
        return


    
    



if __name__ == "__main__":
    main()