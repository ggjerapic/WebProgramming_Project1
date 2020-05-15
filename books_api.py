import requests

def goodreads_api(inp_isbn):
    #res = requests.get("https://api.fixer.io/latest?base=USD&symbols=EUR")
    # test ISBN: 9780312206482, test KEY: I0rXpmFtAcrSCJwLhC0A7g
    # res = requests.get("https://www.goodreads.com/book/review_counts.json",
    #                    params={"key": "KEY", "isbns": "9781632168146"})
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "I0rXpmFtAcrSCJwLhC0A7g", "isbns": inp_isbn})
    data = res.json()
    n_reviews = data['books'][0]['work_ratings_count']
    avg_rating = data['books'][0]['average_rating']
    return n_reviews, avg_rating

    # if res.status_code != 200:
    #     raise Exception("ERROR: API request unsuccessful.")
    # data = res.json()
    # print(data)

if __name__ == "__main__":
    inp_isbn="553803700"
    # inp_isbn="xxx"
    data1, data2 = goodreads_api(inp_isbn)
    print(f"number of reviews: {data1} and average rating: {data2}")