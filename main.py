from collect_sale_links.collect_links import perform_google_search, filter_links


# item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
# item_name = 'Armasight BNVD-51 Gen 3 Pinnacle Night Vision Goggle'
# item_name = 'BOSS StrongBox 7126-7640 - Pull Out Drawer'
item_name = 'Renogy 1.2kW Essential Kit'


def main():
    skip_unfiltered = False
    if not skip_unfiltered:
        unfiltered_link_list = perform_google_search(item_name, 50)
        if not unfiltered_link_list:
            print(f'No search results found for "{item_name}"')
            return
        with open('./printout_data/unfiltered_links.txt', 'w') as file:
            for link in unfiltered_link_list:
                file.write(f'{link}\n')
    else:
        with open('printout_data/unfiltered_links.txt', 'r') as file:
            unfiltered_link_list = file.readlines()

    skip_competitor = False
    if not skip_competitor:
        competitor_link_list = filter_links(unfiltered_link_list, item_name)
        if not competitor_link_list:
            print('No competitors found')
            return
        with open('printout_data/competitor_links.txt', 'w') as file:
            for link in competitor_link_list:
                file.write(f'{link}\n')
    else:
        with open('printout_data/competitor_links.txt', 'r') as file:
            competitor_link_list = file.readlines()


    
    



if __name__ == "__main__":
    main()