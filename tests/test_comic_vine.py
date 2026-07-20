from comic_vine import ComicVine

comic_desc = {
    'description': '<p>Hello comic test with description</p>',
    'issue_number': 72,
    'volume': {
        'name': 'Test comic with desc'
},
    'image': {
       'original_url' : 'https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTMCYaYEiKdNJwgX5Rkoo3TDrKbHOyuLKssj3Cq5yW7Oj3k0EKnaTsQxRhkIJSFqVikp9MsEZHGb4ifgfJ3qjdCVhA'
    }
}

comic_no_desc = {
    'description': '',
    'issue_number': 73,
    'volume': {
    'name': 'Test comic no desc'
},    'image': {
       'original_url' : 'http://t1.gstatic.com/licensed-image?q=tbn:ANd9GcQBmHHHq9Hb_hgCm78dX70sKcoUmJTqYzVsALNOWXvSPKlVf7NPjj5-Fd53nSSJKcVXCO9wQO3ymycfCMf_bt2hV5U'
    }
}

def test_format_comic_no_desc():
    result = ComicVine.prep_content(comic_no_desc)
    assert result[-1]['children'] == ['No discription'], f'Recieved result is {result[-1]['children']}'

def test_format_comic_desc():
    result = ComicVine.prep_content(comic_desc)
    assert result[-1]['children'] == ['Hello comic test with description']