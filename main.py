from collect_sale_links.collect_links import collect_links


item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
# item_name = 'Armasight BNVD-51 Gen 3 Pinnacle Night Vision Goggle'


def main():
    competitor_link_list = collect_links(item_name)
    if not competitor_link_list:
        print('No competitors found')
        return
    



if __name__ == "__main__":
    main()