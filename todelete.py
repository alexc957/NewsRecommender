from articles.models import Article

articles = Article.objects.all()

for i, article in enumerate(articles):
    count = 0
    print(i)
    sim_articles = article.similar_articles.all()[7:]
    for sim_article in sim_articles:
        sim_article.delete()
        count += 1
        if count > 4:
            break

print("done")
