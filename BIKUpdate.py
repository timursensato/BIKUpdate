import os
import urllib.request
import zipfile
import time
import subprocess
import sys

# text to search BIK links in cbr page code
bik_link = '/mcirabis/BIK/bik_dc'

# url link to BIK page
url = 'https://cbr.ru/mcirabis/?PrtId=bic'

# BIK files list in '/Users/TheAceOfSpades/Desktop/izm/' before udpate
bik_files_list = os.listdir('/Users/TheAceOfSpades/Desktop/izm/')
bik_files_list.remove('.DS_Store')


def get_links():
    dlist = []
    cbr_request = urllib.request.urlopen(url)
    cbr_response = cbr_request.read().decode('utf-8')
    # with open('code.txt', 'wb') as fd:
    #     fd.write(cbr_request.text.encode('utf-8'))
    #     fd.close()
    #     cbr_code_file = open('code.txt', 'r')
    #     cbr_code_text = cbr_code_file.read()
    #     cbr_code_file.close()
    i = cbr_response.count(bik_link)
    position = cbr_response.find(bik_link)

    while i != 0:
        create_link = ('http://cbr.ru' + cbr_response[position: position + 38])
        dlist.append(create_link)
        i = i - 1
        position = cbr_response.find(bik_link, position + 1)

    return dlist


def valid_links():
    dlist = get_links()
    print(dlist)
    bik_number = []

    for t in range(len(dlist)):
        bik_number.append(dlist[t][34:47])

    max_of_bik_number = max(bik_number)
    date = max_of_bik_number[5:13]
    return date


def download_zip():
    dwn_list = []
    dlist = get_links()
    date = valid_links()
    zip_list = os.listdir('/Users/TheAceOfSpades/Desktop/Бики для обновления/')
    zip_list.remove('.DS_Store')

    for i in range(len(dlist)):
        dlist_str = dlist[i][27:51]
        if dlist_str not in zip_list:
            if date == dlist[i][39:47]:
                print(dlist[i][27:47] + ' downloaded')
                urllib.request.urlretrieve(dlist[i], '/Users/TheAceOfSpades/Desktop/Бики для обновления/' + dlist_str)
                dwn_list.append(dlist_str)
        elif date == dlist[i][39:47]:
            dwn_list.append(dlist_str)
            print(dlist[i][27:47]+' alredy in /Users/TheAceOfSpades/Desktop/Бики для обновления/')

    print('dwn_list is: ', dwn_list)
    return dwn_list


def zip_extract():
    name_list = []
    dwn_list = download_zip()

    for i in range(len(dwn_list)):
        zipobj = zipfile.ZipFile('/Users/TheAceOfSpades/Desktop/Бики для обновления/' + dwn_list[i])
        zip_file_name_list = zipobj.namelist()
        zip_file_name_list.remove('inf_bik_co.doc')

        for j in zip_file_name_list:
            if '.dbf' in j:
                zipobj.extract(j, '/Users/TheAceOfSpades/Desktop/izm/')
                name_list.append(j)

            if j not in bik_files_list and '.DBF' in j:

                    j1 = j[:7] + 'O.DBF'
                    if j1 in bik_files_list:
                        print('BIK ' + j1 + ' already updated')
                        sys.exit(0)
                    else:
                        zipobj.extract(j, '/Users/TheAceOfSpades/Desktop/izm/')
                        name_list.append(j)
            else:
                print(j + ' already in /Users/TheAceOfSpades/Desktop/izm/')

        zipobj.close()
        subprocess.Popen(["/usr/bin/open", "-W", "-a", '/Applications/TextEdit.app'])
        time.sleep(10)
        subprocess.Popen(["pkill", "-f", "/Applications/TextEdit.app"])

        print(name_list)

        bik_files_list1 = os.listdir('/Users/TheAceOfSpades/Desktop/izm/')
        bik_files_list1.remove('.DS_Store')
        if 'co.dbf' in bik_files_list1:
            bik_files_list1.remove('co.dbf')
            difference = list(set(bik_files_list1) - set(bik_files_list))
        else:
            difference = list(set(bik_files_list1) - set(bik_files_list))

        if len(difference) != 0:
            for t in range(len(difference)):
                if difference[t][-5:] == 'O.DBF':
                    print('BIK '+difference[t]+' updated successfuly')
                else:
                    print('BIK not updated')
        else:
            print('BIK not updated')

zip_extract()




# os.remove('code.txt')




