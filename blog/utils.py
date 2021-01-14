from django.shortcuts import redirect


def valid(form, post):
    if form.is_valid():
        # Create comment object but not save to DB yet
        new_comment = form.save(commit=False)

        # Assign current post to comment
        new_comment.post = post

        # Save comment to DB
        new_comment.save()
        # return redirect('/')
