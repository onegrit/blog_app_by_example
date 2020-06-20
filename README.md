# Django 3 by Example 
## Chapter 2
    功能要点：
    - Sharing posts via email: When readers like an article, they might want to share it with somebody else. 
    You will implement the functionality to share posts via email.通过电子邮件分享帖子
        
    - Adding comments to a post: Many people want to allow their audience to comment on posts and create discussions. 
    You will let your readers add comments to your blog posts.为帖子添加评论
    - Tagging posts: Tags allow you to categorize content in a non-hierarchical manner, using simple keywords. 
    You will implement a tagging system, which is a very popular feature for blogs.标记帖子
    - Recommending similar posts: Once you have a classification method in place, such as a tagging system, 
    you can use it to provide content recommendations to your readers. You will build a system that recommends 
    other posts that share tags with a certain blog post.推荐类似的帖子
## Sharing posts via email
 思路：
 - Create a form for users to fill in their name, their email, the email recipient, and optional comments
 - Create a view in the views.py file that handles the posted data and sends the email
 - Add a URL pattern for the new view in the urls.py file of the blog application
 - Create a template to display the form