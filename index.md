---
layout: default
title: Главная
---

# Самые новые технологии

{% assign files = site.static_files | where: "path", "/content" %}
{% assign latest = site.static_files | sort: "modified_time" | last %}

{% capture latest_path %}{{ latest.path }}{% endcapture %}
{% include_relative {{ latest_path }} %}
