---
layout: default
title: Архив
---

# Архив технологий

{% for file in site.static_files %}
  {% if file.path contains '/content/' %}
    - [{{ file.name | remove: '.md' }}](.{{ file.path }})
  {% endif %}
{% endfor %}
