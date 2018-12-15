module TextsHelper
  def recommendation_for(text)
    result = `python /Users/liuyancen/Desktop/test.py `+text
  end
end
