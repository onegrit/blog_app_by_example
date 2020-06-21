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
 
## Creating a comment system
  - 显示comments总数
  - 显示comment 列表
  - 显示空的comment准备接收用户提交Comment
  思路：
  You will create a comment system wherein users will be able to comment on posts.
  To build the comment system, you need to do the following:
  - Create a model to save comments
  - Create a form to submit comments and validate the input data.
  - Add a view that process the form and saves a new comment to the database.
  - Edit the post detail to display the list of comments and the form to add a new comment.
## Tagging Posts
   需求：
    - 用户可以列出（过滤）与打了该Tag的所有Posts
   思路：
   - It takes an optional tag_slug parameter that has a None default value. This parameter will be passed in the URL.
   - Inside the view, you build the initial QuerySet, retrieving all published posts, and if there is a given tag slug, 
   you get the Tag object with the given slug using the get_object_or_404() shortcut.
   - Then, you filter the list of posts by the ones that contain the given tag. Since this is a many-to-many relationship, you have to filter posts by
tags contained in a given list, which, in your case, contains only one element. You use the __in field lookup. Many-to-many relationships occur
when multiple objects of a model are associated with multiple objects of another model. In your application, a post can have multiple tags and a
tag can be related to multiple posts.
## 检索类似的帖子