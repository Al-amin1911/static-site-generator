# static-site-generator

#What Is a Static Site Generator?
A static site generator takes raw content files (like Markdown and images) and turns them into a static website (a mix of HTML and CSS files).

# Markdown
Writing Markdown is pure bliss. Markdown is a less-verbose markup language designed for ease of writing. The trouble is web browsers don't understand Markdown. They only understand HTML and CSS. The #1 job of a static site generator is to convert Markdown into HTML.
Instead of writing a verbose HTML list:
```HTML
<ul>
  <li>I really</li>
  <li>hate writing</li>
  <li>in raw html</li>
</ul>
```
We can write this in md
```
- I really
- hate writing
- in raw html
```
This static site generator will take a directory of Markdown files (one for each web page), and build a directory of HTML files. Because I am not a savage, I'll also include a single CSS file to style the site.
