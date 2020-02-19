from Infrastructures.Repositories import HashtagRepository as htgsRepo, FollowsRepository as flwsRepo
from Infrastructures.Repositories import FollowersRepository as flwersRepo
from Services.GetUserService import GetUsers
from Models.Follower import Follower
from Models.Follow import Follow
from datetime import datetime
import time
import random

def FollowHashTag(acc, hashtag, bot):
    # Khai báo
    getUserSv = GetUsers(bot)
    # Lưu hashtag vào bảng HashTag
    # - Kiểm tra đã có hashtag này chưa
    # + Nếu chưa => lưu hashtag và lấy hashtagId
    # + Nếu có => lấy hashtagId
    htgId = htgsRepo.ReadHashtagId(hashtag.Name)
    if htgId == None:
        hashtag = htgsRepo.AddHashtag(hashtag)
    else:
        hashtag.Id = htgId
    # Quét user theo hashtag
    # - Kiểm tra đã có user của hashtag này chưa
    followers = flwersRepo.ReadFollowers(hashtag.Id)
    users = getUserSv.GetUsersFromHastag(hashtag.Name)
    # + Nếu chưa => Quét thông tin và lưu vào user theo hashtagId
    if len(followers) == 0:
        for user in users:
            flr = Follower(userName = user.UserName, userId = user.UserId, hashtagId = hashtag.Id)
            flwersRepo.AddFollower(flr)
    # + Nếu đã có => Quét lại và lưu những user chưa có trong danh sách
    else:
        for user in users:
            ok = True # Dùng để xác định Follower này đã tồn tại chưa (User-HashTag)
            for flwer in followers:
                if user.UserId == flwer.UserId:
                    ok = False
                    break                
            if ok:
                flr = Follower(userName=user.UserName, userId = user.UserId, hashtagId = hashtag.Id)
                flwersRepo.AddFollower(flr)
    # Lưu user của hashtag vào danh sách follow của Account
    followers = flwersRepo.ReadFollowers(hashtag.Id) # Đọc lại tất cả follower theo hashtag sau khi thêm
    # - Kiểm tra đã có hashtag này trong ds follow của account chưa
    follows = flwsRepo.ReadFollowsHtg(acc.Id, hashtag.Id)
    # + Nếu chưa => thêm tất cả user-hashtag này vào bảng follow
    if len(follows) == 0:
        for fler in followers:
            fl = Follow(accountId = acc.Id, followerId = fler.Id, status = False)
            flwsRepo.AddFollow(fl)
    # + Nếu đã có => Chỉ thêm những user-hashtag chưa có vào bảng follow
    else:
        for follower in followers:
            ok = True
            for follow in follows:
                if follower.Id == follow.FollowerId:
                    ok = False
                    break
            if ok:
                fl = Follow(accountId=acc.Id, followerId=follower.Id, status=False)
                flwsRepo.AddFollow(fl)
    # Cho Account Follow danh sách các user-hashtag chưa dùng trong bảng follow
    follows = flwsRepo.ReadFollowsStatus(acc.Id, False)
    # - Follow các user chưa sử dụng
    # - Cập nhật trạng thái sử dụng các user + thêm thời gian follow 
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    for fl in follows:
        bot.follow(fl.Follower.UserId)
        flwsRepo.UpdateStatus(fl.Id, True)
        flwsRepo.UpdateDateFollow(fl.Id, date)
        followDelayTime = random.randint(200, 300)
        time.sleep(followDelayTime)

def AccFollow(accId, bot):
    # Cho Account Follow danh sách các user-hashtag chưa dùng trong bảng follow
    follows = flwsRepo.ReadFollowsStatus(accId, False)
    # - Follow các user chưa sử dụng
    # - Cập nhật trạng thái sử dụng các user + thêm thời gian follow 
    for fl in follows:
        bot.follow(fl.Follower.UserId)
        flwsRepo.UpdateStatus(fl.Id, True)