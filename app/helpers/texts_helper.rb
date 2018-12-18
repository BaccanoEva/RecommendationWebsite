require 'rubygems'
require 'json'
require 'pp'
module TextsHelper
  def recommendation_for(text)
    #result = system `python /Users/liuyancen/Desktop/test.py`,"try"
    #result = system("python /Users/liuyancen/Desktop/test.py try")
    #python_cmd = Escape.shell_command(['python', "/Users/liuyancen/Desktop/test.py"]).to_s
    #system python_cmd
    #print python_cmd
    a = text.question
    #pp a
    result = `python test_2.py '#{a}'`
    pp "result ="
    pp result
    return JSON.parse(File.read('test.json'))
    #return JSON.parse(json)
    #return obj
  end
end
