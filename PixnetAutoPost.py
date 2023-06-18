from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
#載入相關模組

options = Options()
options.chrome_executable_path = "E:\sideproject\chromedriver.exe"
#設定Chrome Driver的執行檔路徑

titlelist = ['連續1','連續2','連續3']
contentdict = {'連續1':"內容1",
            '連續2':"內容2",
            '連續3':"內容3"}
#載入標題list及內容dictionary
#以上是提供測試用的內容，本身程式是另外匯入txt或csv檔

youremail = input('請輸入帳號:')
yourpassword = input('請輸入密碼:')
#執行程式時會在終端機先要求使用者輸入痞客邦的帳號及密碼
#之後可能會利用Python或PyGame等其他功能設計前端界面
#用於輸入帳號密碼及匯入csv檔案

def AutoPost(titlelist,contentdict,youremail,yourpassword):

    driver = webdriver.Chrome(options=options)
    driver.maximize_window() #視窗最大化
    #建立 driver 物件實體(瀏覽器本體)，用程式操作瀏覽器運作

    driver.get("https://www.pixnet.net")
    time.sleep(2)
    #連線到痞客邦，並等2秒讓網頁開啟

    loginBtn = driver.find_element(By.CLASS_NAME,"login")
    loginBtn.click()
    time.sleep(2)
    #找到登入按鈕點擊後，等2秒

    UsernameInput = driver.find_element(By.NAME,"email")
    PasswordInput = driver.find_element(By.NAME,"password")
    UsernameInput.send_keys(youremail)
    PasswordInput.send_keys(yourpassword)
    signinBtn = driver.find_element(By.XPATH,"/html/body/div/div/div/main/section[2]/form/button")
    signinBtn.send_keys(Keys.ENTER)
    time.sleep(1)
    #輸入帳號密碼並登入，等1秒

    ArticlePost = driver.find_element(By.CLASS_NAME,"create-article")
    ArticlePost.click()
    time.sleep(1)
    #連線到發文後台，等1秒

    #這裡使用for迴圈，由於文章標題與文章內容數量固定
    #因此當標題list的每一個項目跑完，也代表內容全部跑完了
    #所以不需要設定發文次數也能自動執行全部內容
    for AllArticle in titlelist:
        Title = driver.find_element(By.ID,"editArticle-header-title")
        ModelofPost = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div[2]/pix-ck-editor/div[2]/div/span[1]/span[2]/span[10]")
        Title.send_keys(AllArticle)
        #標題用檔案或一個titlelist直接導入
        #並用for迴圈將標題的list元素一個一個放入send_keys裡

        ModelofPost.click()
        ArticleModel = driver.find_element(By.XPATH,"/html/body/pix-plugins-panel/div/div/ul[2]/li[2]/pix-plugins-panel-btn[2]/a")
        ArticleModel.click()
        #設定標題後進到擴充元件的文字編輯器
        time.sleep(1)

        ##此處因為痞客邦的內容框架屬於虛擬框架(iframe)
        ##必須使用switch_to來進入框架內
        driver.switch_to.default_content()
        framename = driver.find_element(By.NAME,'addon836')
        driver.switch_to.frame(framename)
        #以上是進入虛擬框架內部

        content = driver.find_element(By.XPATH,"/html/body/form/div[1]/div/table/tbody/tr[2]/td/textarea")
        content.send_keys(contentdict[AllArticle])
        #調整框架完畢後執行整個輸入內容的動作
        #利用字典的方式，將相對應標題的內容丟入內容欄位中

        contentOK = driver.find_element(By.ID,"popup-submit-btn")
        contentOK.click()
        time.sleep(0.5)
        #內容輸入完畢後點擊確認

        driver.switch_to.default_content()
        #回到主框架

        ArticleSetting = driver.find_element(By.ID,"editArticle-setting")
        ArticleSetting.click()
        time.sleep(0.5)
        categories = driver.find_element(By.ID,"site-categories")
        categories.click()
        time.sleep(0.1)
        ArticleType = driver.find_element(By.XPATH,"/html/body/dialog/div/form/div/div[2]/div[2]/div[1]/div/select/option[41]")
        ArticleType.click()
        Btn_OK = driver.find_element(By.XPATH,"/html/body/dialog/div/form/footer/button[2]")
        Btn_OK.click()
        time.sleep(0.5)
        #由於痞客邦要求用戶一定要設定分類，因此找到設定標籤並點擊
        #之後彈出視窗選擇分類確認後回到發布頁面
        #由於分類有40多種，目前先單一標籤統一發文

        Btn_post = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div[3]/table/tbody/tr/td[2]/button[4]")
        Btn_post.click()
        time.sleep(5)
        #點選發布文章之後點擊確認，等5秒確定文章發布有跑完(等久一點避免網路速度影響)
        driver.get("https://panel.pixnet.cc/#/create-article")
        time.sleep(2)
        count += 1
        #重新連回發布文章的網址，回到迴圈開頭
    
    driver.close()
    #發文完畢才關閉視窗

AutoPost(titlelist,contentdict,youremail,yourpassword)
