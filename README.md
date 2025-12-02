# Network

## Intro

This is the Project 4 from **CS50's Web Programming with Python and JavaScript**.  
Instructors: Brian Yu and David J. Malan

### Summary

The goal of this activity is to creat a social media, applying the knowledge acquired from the complete course.

### Specifications

#### New Post
- [x] Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
- [x] The screenshot at the top of this specification shows the “New Post” box at the top of the “All Posts” page. You may choose to do this as well, or you may make the “New Post” feature a separate page.
#### All Posts
- [x] The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.
- [x] Each post should include the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later).
#### Profile Page
- [x] Clicking on a username should load that user’s profile page. This page should: 
- [x] Display the number of followers the user has, as well as the number of people that the user follows.
- [x] Display all of the posts for that user, in reverse chronological order.
- [x] For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.
#### Following
- [x] The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.
This page should behave just as the “All Posts” page does, just with a more limited set of posts.
- [x] This page should only be available to users who are signed in.
### Pagination: 
- [x] On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well. See the Hints section for some suggestions on how to implement this.
### Edit Post: 
- [x] Users should be able to click an “Edit” button or link on any of their own posts to edit that post.
- [x] When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a textarea where the user can edit the content of their post.
The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.
For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts.
### “Like” and “Unlike”: 
- [x] Users should be able to click a button or link on any post to toggle whether or not they “like” that post. 
- [x] Using JavaScript, you should asynchronously let the server know to update the like count (as via a call to fetch) and then update the post’s like count displayed on the page, without requiring a reload of the entire page.

### Links

- [🔗 Project Specification](https://cs50.harvard.edu/web/projects/4/network/)  


### Author
Rafael Mourato (Rafael.mourato@hotmail.com) - Student of Informational Systems at Federal University of Pernambuco.

### License
This project is for educational purposes only and is not affiliated with any company.
