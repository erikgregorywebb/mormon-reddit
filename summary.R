library(tidyverse)
library(readxl)

# import
setwd("~/Documents/Python/mormon-reddit")
excel_file = 'mormon-reddit copy.xlsx'
submissions = read_excel(excel_file, sheet = 'submissions')
comments = read_excel(excel_file, sheet = 'comments')
redditors = read_excel(excel_file, sheet = 'redditors')

# summarize submissions
submissions %>%
  group_by(author_name, subreddit) %>%
  count() %>%
  spread(subreddit, n, fill = 0) %>%
  mutate(total = exmormon + latterdaysaints + lds + mormon) %>%
  arrange(desc(total))

# summarize comments
comments %>%
  group_by(comment_author, subreddit) %>%
  count() %>%
  spread(subreddit, n, fill = 0) %>%
  mutate(total = exmormon + latterdaysaints + lds + mormon) %>%
  arrange(desc(total))
