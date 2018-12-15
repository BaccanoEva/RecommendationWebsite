class TextsController < ApplicationController
  def new
    @text = Text.new
  end

  def show
    @text = Text.find(params[:id])
  end

  def create
    @text = Text.new(text_params)    # 不是最终的实现方式
    if @text.save
      # 处理注册成功的情况
      redirect_to @text
    else
      render 'new'
    end
  end
    def text_params
      params.require(:text).permit(:question)
    end
end
