<?php

/**
 * @name ActivityController
 * @author chenshigang
 * @desc 活动控制器
 */
class ActivityController extends Controller {

    private $activityModel;
    private $activityUserModel;
    private $_probabilityTotal = 100;
    private static $code = array(
        2 => 'Y01N8LYD',
        3 => 'JK6XBUAJ',
        4 => '7G51RD5P',
        5 => 'XZWTGYCT',
    );

    //验证抽奖资格，ajax
    public function ajaxLotteryQualificationAction() {
        $userInfo = $this->checkUserLogin(true);
        if (empty($userInfo)) {
            $this->outPut('', '用户登录', 2);
        }
        $uid = $userInfo['uid'];
        //2018年1月29日 16:18:43 用户相关信息传入
        $params['userType'] = $userInfo['userType'];
        $params['vip_pause'] = $userInfo['vip_pause']['is_pause'];

        $activityId = $this->get('activity_id', '');
        if (empty($activityId)) {
            $this->outPut('', '参数错误', -1);
        }

        $this->activityModel = new Activity_ActActivityModel();
        $activity = $this->activityModel->getActivityByActivityId($activityId);
        if (!$this->activityModel->isOnline($activity)) {
            $this->outPut('', '活动已结束', -1);
        }

        $this->activityUserModel = new Activity_ActActivityUserModel();
        $freeCntLeft = $this->activityUserModel->getFreeCntLeftByActivityIdAndUid($activityId, $uid, $params);
        if ($freeCntLeft === false) {
            $this->outPut('', '请求失败，请稍后重试', -1);
        }
        //免费次数
        if ($freeCntLeft > 0) {
            $data = array(
                'lottery_type' => 1,
                'lottery_desc' => '免费抽奖',
            );
            $this->outPut($data, '', 0);
        } elseif ($freeCntLeft < 1 && $activity['consume_points'] == 2) {
            $this->outPut('', '您好，您今日的免费抽奖次数已用完。', -1);
        }

        $userModel = new UserCenter_UserModel();
        $userInfo = $userModel->getUserInfo($uid);
        //免费用完，使用瑜币
        if ($userInfo['TotalScore'] >= $activity['score_cost']) {
            $data = array(
                'lottery_type' => 2, //瑜币抽奖
                'lottery_desc' => '瑜币抽奖', //瑜币抽奖
            );
            $this->outPut($data, '', 0);
        }
        //瑜币不足，去赚瑜币
        $data = array(
            'lottery_type' => 3,
            'lottery_desc' => '去赚瑜币',
        );
        $this->outPut($data, '', 0);
    }

    /**
     * 获取启动页面信息
     * url: http://192.168.200.168/yoga/home/loading
     */
    public function indexAction() {
        $paramsSign = $this->get('param_sign') !== ''?Util::UIDDecrypt($this->get('param_sign')):'';
        $activityId = (int)$this->get('activity_id', '');
        $channel = $this->get('channel', '');
        $type = $this->get('type', 0);
        $sid = $this->get('sid', 0); //登陆和未登录都可展示
        DBC::requireNotEmpty($activityId,'参数错误',-1);

        $this->activityModel = new Activity_ActActivityModel();
        $activity = $this->activityModel->getActivityByActivityId($activityId);
        DBC::requireNotEmpty($activity['id'],'该活动已被删除');
        if (empty($activity['page_title'])) {
            $activity['page_title'] = Library_Activity::PAGE_TITLE_DEFAULT_TYPE_MOBILE;
        }
        // 图片处理为无协议的
        if (!empty($activity) && is_array($activity)) {
            $activity = array_merge($activity, Image::batchConvertNoProtocol([
                'home_page_bg_img' => $activity['home_page_bg_img'],
                'home_page_bg_img_head' => $activity['home_page_bg_img_head'],
                'home_page_bg_img_body' => $activity['home_page_bg_img_body'],
                'home_page_bg_img_foot' => $activity['home_page_bg_img_foot'],
                'result_page_bg_img' => $activity['result_page_bg_img'],
                'image_ext' => $activity['image_ext'],
                'image_phone' => $activity['image_phone'],
                'image_pad' => $activity['image_pad'],
            ]));
        }

        //  @change 应运营的需求，手机号领奖需要进行参数验证，其他活动模式暂时忽略(params_sign生成：Util::UIDEncrypt(activity_id=XXX))    @author KK      @time  2019年10月29日
        if ($activityId > Library_Activity::MAX_ACTIVITY_ID_BY_MOBILE_TO_SIGN && (int)$activity['type'] === Library_Activity::ACTIVITY_TYPE_MOBLIE ){
            DBC::requireTrue($paramsSign === 'activity_id='.$activityId,'参数验签名未通过！');
        }

        $infoActivity = (new Activity_ActPreConditionModel())->getPreConditionByActivityId($activityId);
        $activity = array_merge($activity,$infoActivity);
        $activity['is_login'] = $sid == 0 ? 0 : 1;
        $judge_end = $this->activityModel->_judge_end($activity['type']);
        if ($judge_end && !$this->activityModel->isOnline($activity) && !in_array($activity['type'],
                [Library_Activity::ACTIVITY_TYPE_MOBLIE, Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_ANDRIOD, Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_IOS], true)) {
            $this->outPut('', '活动已结束', -1);
        }

        if ($sid && !in_array($activity['type'], array(Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_ANDRIOD, Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_IOS))) {
            if ($this->activityModel->needLogin($activity)) {
                $userInfo = $this->checkUserLogin(true);
                if (empty($userInfo)) {
                    $this->outPut('', ' 用户未登录', 2);
                }
                $uid = $userInfo['uid'];
                //2018年1月29日 16:18:43 用户相关信息传入
                $params['userType'] = $userInfo['userType'];
                $params['vip_pause'] = $userInfo['vip_pause']['is_pause'];
                $nickName = $userInfo['nickName'];
                $activityId = $this->get('activity_id', '');
                if (empty($activityId)) {
                    $this->outPut('', '参数错误', -1);
                }
            }
        }
        $prizeModel = new Activity_ActPrizeModel();
        $prizeList = $prizeModel->getPrizeListByActivityId($activityId);
        foreach ($prizeList as &$one) {
            unset($one['probability']);
            unset($one['internal_uids']);
            unset($one['prize_cnt']);
            unset($one['prize_cnt_left']);
            if ($one['type'] == Library_Activity::PRIZE_ENTITY) {
                $activity['has_entity'] = 1;    //判断奖品中是否含有实物
            }

            // 处理图片为无协议
            if (!empty($one['image'])) {
                $one['image'] = Image::convertNoProtocol($one['image']);
            }
            if (!empty($one['image_pad'])) {
                $one['image_pad'] = Image::convertNoProtocol($one['image_pad']);
            }
        }

        $activity['prize_list'] = $prizeList;
        $opinion_url = Yaf_Application::app()->getConfig()->application->activity_opinion_url;
        switch ($activity['type']) {
            case Library_Activity::ACTIVITY_TYPE_LOTTY :
                $this->activityUserModel = new Activity_ActActivityUserModel();
                $freeCntLeft = $this->activityUserModel->getFreeCntLeftByActivityIdAndUid($activityId, $uid, $params);
                if ($freeCntLeft === false) {
                    $this->outPut('', '请求失败，请稍后重试', -1);
                }
                //免费次数
                if ($freeCntLeft < 1) {
//                     $userModel = new UserCenter_UserModel();
//                     $userInfo = $userModel->getUserInfo($uid);
                    //免费用完，使用瑜币
                    if ($userInfo['points'] < $activity['score_cost']) {
                        $this->outPut($activity, '去赚瑜币', 1);
                        return true;
                    }
                }
                break;
            case Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_ANDRIOD:
                $activity['share_url'] = $opinion_url . 'comments/andr.html?activity_id=' . $activityId . '&channel=' . $channel;
                $activity['content']  = json_decode($activity['content'], true);
                break;
            case Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_IOS:
                $activity['share_url'] = $opinion_url . 'comments/ios.html?activity_id=' . $activityId . '&channel=' . $channel;
                $activity['content']  = json_decode($activity['content'], true);
                break;
            case Library_Activity::ACTIVITY_TYPE_INVITE_USER:
                $invite_url = Yaf_Application::app()->getConfig()->application->activity_invite_user;
                $inviteUserModel = new Activity_InviteUserModel();
                $activity['top_list'] = $inviteUserModel->getTopUserList($activityId);
                $activity['total'] = count($activity['top_list']);
                $activity['exp'] = $inviteUserModel->getDetailInfo($activityId, $uid, $nickName);
                $activity['share_url'] = $invite_url . '?activity_id=' . $activityId . '&channel=' . $channel . '&from_uid=' . $uid . '&activity_type=' . Library_Activity::ACTIVITY_TYPE_INVITE_USER . '&type=' . $type;
                break;
            case Library_Activity::ACTIVITY_TYPE_LOTTERY_DRAW_SCORE:
                $this->activityUserModel = new Activity_ActActivityUserModel();
                $activity['free_cnt_left'] = $this->activityUserModel->getUserFreeCnt($activity, $uid, $params);
                $activity['vip_pause'] = $userInfo['vip_pause']['is_pause'];
                break;
        }

        $activity['has_expire'] = $activity['end_time'] < time();
        $this->outPut($activity, '', 0);
    }

    //参与活动的入口
    public function lotteryAction() {
        $paramsSign = $this->post('param_sign') !== ''?Util::UIDDecrypt($this->post('param_sign')):'';
        $activityId = (int)$this->get('activity_id', '');
        DBC::requireNotEmpty($activityId, '参数错误', -1);
        Log::trace('lottery===>' . json_encode($_REQUEST));
        //写好评活动
        $data['name'] = $this->post('name', '');
        $data['telephone'] = $this->post('telephone', '');
        $data['address'] = $this->post('address', '');
        $data['channel'] = $this->post('channel', '');

        $this->activityModel = new Activity_ActActivityModel();
        $activity = $this->activityModel->getActivityByActivityId($activityId);
        DBC::requireTrue($this->activityModel->isOnline($activity), '活动已结束', -1);

        $this->activityUserModel = new Activity_ActActivityUserModel();
        if ($this->activityModel->needLogin($activity)) {
            $data['user'] = $this->checkUserLogin(true);
            DBC::requireNotEmpty($data['user'], '用户未登陆', 2);

            $uid = $data['user']['uid'];
            if (!in_array($activity['type'], array(Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_ANDRIOD, Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_IOS))) {
                //2018年1月29日 16:18:43 用户相关信息传入
                $params['userType'] = $data['user']['userType'];
                $params['vip_pause'] = $data['user']['vip_pause']['is_pause'];
                $freeCntLeft = $this->activityUserModel->getFreeCntLeftByActivityIdAndUid($activityId, $uid, $params);
                if ($activity['type'] == Library_Activity::ACTIVITY_TYPE_LOTTERY_DRAW_SCORE) {
                    DBC::requireTrue($freeCntLeft >= 0, '您好，您今日的免费抽奖次数已用完。', -1);
                } else {
                    DBC::requireTrue(!($freeCntLeft < 1 && $activity['consume_points'] == 2), '您好，您今日的免费抽奖次数已用完。', -1);
                }
                DBC::requireTrue($freeCntLeft !== false, '请求失败，请稍后重试', -1);
            }
        }
        switch ($activity['type']) {
            case Library_Activity::ACTIVITY_TYPE_LOTTY:
                // 开始摇奖
                $ret = $this->wantPrize($freeCntLeft, $data['user'], $activity); //2018年1月29日 16:30:08 water 传入用户信息 减少内部用户调用
                break;

            case Library_Activity::ACTIVITY_TYPE_MOBLIE:
                //  @change 应运营的需求，手机号领奖需要进行参数验证，其他活动模式暂时忽略(params_sign生成：Util::UIDEncrypt(activity_id=XXX))    @author KK      @time  2019年10月29日
                if ($activityId > Library_Activity::MAX_ACTIVITY_ID_BY_MOBILE_TO_SIGN ){
                    DBC::requireTrue($paramsSign === 'activity_id='.$activityId,'参数验签名未通过！');
                }
                // 填手机号领奖
                $data['mobile'] = $this->post('mobile', '');
                DBC::requireNotEmpty($data['mobile'], '参数错误', -1);
                DBC::requireTrue(Util::checkPhone($data['mobile']), '您填写的手机号格式不正确', -1);
                $this->checkUserIsExistsLogoff($data['mobile'], Library_User::CHECK_USER_LOGOFF_TYPE_BIND_VALUE);
                $ret = $this->claimPrize($activity, $data);
                break;
            case Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_ANDRIOD:
                $data['image'] = $this->post('image', '');
                DBC::requireNotEmpty($data['image'], '参数错误', -1);
                $ret = $this->activityUserModel->writeHignOpinion($activity, $uid, $data);
                break;
            case Library_Activity::ACTIVITY_TYPE_HIGH_OPINION_IOS:
                $data['image'] = $this->post('image', '');
                DBC::requireNotEmpty($data['image'], '参数错误', -1);
                $ret = $this->activityUserModel->writeHignOpinion($activity, $uid, $data);
                break;
            case Library_Activity::ACTIVITY_TYPE_LOTTERY_DRAW_SCORE:
                $ret = $this->wantScorePrize($uid, $activity);
                break;
            default:
                $ret = array(
                    'status' => -1,
                    'msg' => '未知活动！'
                );
        }

        $this->outPut($ret['data'], $ret['msg'], $ret['status']);
    }

    //大转盘()
    private function wantScorePrize($uid, $activity) {
        //用户信息;
        $userModel = new UserCenter_UserModel();
        $userInfo = $userModel->getUserInfo($uid);
        $userInfo['uid'] = $userInfo['AccountId'];
        $userInfo['points'] = $userInfo['TotalScore'];
        $activityId = $activity['id'];
        //奖品信息
        $prizeModel = new Activity_ActPrizeModel();
        $prizeList = $prizeModel->getPrizeListByActivityId($activityId);
        $prizeArr = array();
        $prizeMap = array();
        $probabilityTotal = 0;
        $prizeList = $this->lotteryStrategy($uid, $activityId, $prizeList, $activity);
        $prizeNotWinner = '';
        foreach ($prizeList as $prize) {
            $prizeArr[$prize['id']] = $prize['probability'];
            $prizeMap[$prize['id']] = $prize;
            $probabilityTotal += $prize['probability'];
            if ($prize['type'] == Library_Activity::PRIZE_NOT_WINNING) { //未中奖奖品
                $prizeNotWinner = $prize['id'];
            }
        }
        $prizeArr['other'] = ($this->_probabilityTotal - $probabilityTotal) > 0 ? $this->_probabilityTotal - $probabilityTotal : 0;
        $arrIndex = Util::getRand($prizeArr, $activity, $prizeNotWinner);
        $prize = null;
        if ($arrIndex == 'other') { //此次没有中奖
            $result['status'] = 3;
            $result['msg'] = array_rand(Library_Activity::$noPrizeContent);
            $result['data'] = '';
        } else {//中奖了
            $prize = $prizeMap[$arrIndex];
            $prizeData = array(
                'prize_id' => $prize['id'],
                'grade' => $prize['grade'],
                'name' => $prize['name'],
                'type' => $prize['type'],
                'push_content' => $prize['push_content']
            );
            $result['status'] = 0;
            $result['msg'] = $prizeData['push_content'];
            $result['data'] = $prizeData;
        }

        //记录抽奖行为
        $userActionLogActivityModel = new Activity_UserActionLogActivityModel();
        $channel = $this->get("channel", ''); //客户来源渠道
        $version = $this->get("version", '');  //版本
        $arr = array(
            'uid' => $uid,
            'activity_id' => $activityId,
            'points' => 0,
            'channel' => $channel,
            'version' => $version,
        );
        $userActionLogActivityId = $userActionLogActivityModel->addActionLog($arr);

        //记录中奖用户
        if ($prize) {
            switch ($prize['type']) {
                case Library_Activity::PRIZE_POINTS :
                    $score2Add = intval($prize['value']);
                    if ($score2Add > 0) {
                        $arr = array(
                            'uid' => $uid,
                            'activity_id' => $activityId,
                            'points' => $score2Add,
                            'channel' => $channel,
                            'version' => $version,
                            'status' => 0,
                        );
                        $userActionLogActivityId = $userActionLogActivityModel->addActionLog($arr);
                        $userModel->updateUserPointInfo($uid, $score2Add, Library_ActionLog::PRIZE, Library_ActionLog::POINTS_INCREASE, $userActionLogActivityId);
                    }
                    break;
                case Library_Activity::PRIZE_VIP_MONTH :
                case Library_Activity::PRIZE_VIP_DAY :
                    $vip_duration_type = Library_Activity::$activity_prize_type_convert[$prize['type']];
                    //查询活动信息 alex
                    $extension = [
                        'operator_id' => $activity['operator_id'],
                        'business_line' => $activity['business_line'],
                        'category_item' => $activity['category_item']
                    ];
                    $userModel->setVipFlexible($vip_duration_type, $prize['value'], $uid, '活动奖励', Library_User::USER_VIP_SOURCE_TYPE_ACTIVITY, $activityId, Library_User::USER_TYPE_VIP, 1, $extension);

                    break;
                case Library_Activity::PRIZE_COUPONS:
                    $rs = $prizeModel->getOneCoupons($activityId, $prize['id'], $prize['push_content'], $uid);
                    $result['msg'] = $rs['msg'];
                    $result['code'] = $rs['code'];
                    break;
            }
            //剩余奖品数减一
            $prizeModel->reducePrizeCntLeft($prize['id']);
            $arr = array(
                'user_action_log_32_id' => $userActionLogActivityId,
                'prize_id' => $prize['id'],
                'activity_id' => $activityId,
                'prize_name' => $prize['name'],
                'user_name' => $userInfo['FirstName'],
                'uid' => $uid,
            );
            $winnerModel = new Activity_ActWinnerModel();
            //统计用户信息
            $arr['channel'] = $channel;
            $arr['user_first_name'] = $userInfo['FirstName'];
            if (Util::isIOSChannel()) {
                $arr['platform'] = '2';
            } else {
                $arr['platform'] = '1';
            }
            $arr['version'] = $version;
            if ($prize['type'] != Library_Activity::PRIZE_NOT_WINNING) {
                $winnerModel->addWinner($arr);
            }
            //发送推送消息
            $servicePushSend = new Service_Service_Push_Send([$uid],'恭喜你，中奖了', $result['msg']);
            $servicePushSend->setExtraParams(['sign_id' => Library_Push::SIGN_ID_ACTIVITY_TURNTABLE_WIN]);
            if (isset($result['code'])) {
                $servicePushSend->setExtraParams(['link_type' => Library_Common::PUSH_LINK_TYPE_CODE, 'link' => $result['code']]);
            }
            if (!empty($result['msg']) && $arrIndex != 'other' && $prize['type'] != Library_Activity::PRIZE_NOT_WINNING) {
                if ($activity['is_three_party'] == 2 && !empty($prize['link_url'])) {  //第三方，通过内链发送
                    $servicePushSend->setExtraParams(['link_type' => $prize['link_type'], 'link' => $prize['link_url']]);
                }

                $servicePushSend->sendPush();
            }
        }
        // 更新促活活动抽奖状态
        (new Service_Service_Activity_Promote())->updateLotteryStatus($uid, $activityId);
        // 新用户任务领奖
        (new Service_Service_Activity_NewPeople())->receiveGift($uid, 4);
        return $result;
    }

    //摇奖
    private function wantPrize($freeCntLeft, $userInfo, $activity) {
        $scoreCost = 0;
        $userModel = new UserCenter_UserModel();
//         $userInfo = $userModel->getUserInfo($uid);
        $uid = $userInfo['uid'];
        //免费次数用完，使用瑜币
        if ($freeCntLeft < 1) {
            //获取用户瑜币
            $score = $userInfo['points'];
            $scoreCost = $activity['score_cost'];
            if ($score < $scoreCost) {
                return array(
                    'status' => 2,
                    'msg' => '瑜币不足',
                );
            }
        }
        $activityId = $activity['id'];
        //奖品信息
        $prizeModel = new Activity_ActPrizeModel();
        $prizeList = $prizeModel->getPrizeListByActivityId($activityId);

        $prizeArr = array();
        $prizeMap = array();
        $probabilityTotal = 0;
        $prizeList = $this->lotteryStrategy($uid, $activityId, $prizeList);
        foreach ($prizeList as $prize) {
            $prizeArr[$prize['id']] = $prize['probability'];
            $prizeMap[$prize['id']] = $prize;
            $probabilityTotal += $prize['probability'];
        }
        $prizeArr['other'] = ($this->_probabilityTotal - $probabilityTotal) > 0 ? $this->_probabilityTotal - $probabilityTotal : 0;
        $arrIndex = Util::getRand($prizeArr);

        $prize = null;
        if ($arrIndex == 'other') { //此次没有中奖
            $result['status'] = 3;
            $result['msg'] = '没有中奖';
            $result['data'] = '';
        } else {//中奖了
            $prize = $prizeMap[$arrIndex];
            $prizeData = array(
                'prize_id' => $prize['id'],
                'grade' => $prize['grade'],
                'name' => $prize['name'],
                'type' => $prize['type'],
                'desc' => $prize['desc'],
            );
            if ($prizeData['type'] == 2) {
                $prizeData['desc'] .= '瑜币';
            }
            $result['status'] = 0;
            $result['msg'] = '恭喜你中奖了';
            $result['data'] = $prizeData;
        }

        //记录抽奖行为
        $userActionLogActivityModel = new Activity_UserActionLogActivityModel();
        $channel = $this->get("channels", ''); //客户来源渠道
        $version = $this->get("version", '');  //版本
        $arr = array(
            'uid' => $uid,
            'activity_id' => $activityId,
            'points' => $scoreCost,
            'channel' => $channel,
            'version' => $version,
        );
        $userActionLogActivityId = $userActionLogActivityModel->addActionLog($arr);

        //瑜币摇奖扣除瑜币
        if ($scoreCost > 0) {
            $userModel->updateUserPointInfo($uid, $scoreCost, Library_ActionLog::PRIZE, Library_ActionLog::POINTS_REDUCE, $userActionLogActivityId);
        } else {//免费摇奖扣除免费次数
            $this->activityUserModel->setFreeCntLeftByActivityIdAndUid($activityId, $uid);
        }

        //记录中奖用户
        if ($prize) {
            if ($prize['type'] == 2) {//瑜币,立马冲上
                $score2Add = intval($prize['desc']);
                if ($score2Add > 0) {
                    $arr = array(
                        'uid' => $uid,
                        'activity_id' => $activityId,
                        'points' => $score2Add,
                        'channel' => $channel,
                        'version' => $version,
                        'status' => 0,
                    );
                    $userActionLogActivityId = $userActionLogActivityModel->addActionLog($arr);
                    $userModel->updateUserPointInfo($uid, $score2Add, Library_ActionLog::PRIZE, Library_ActionLog::POINTS_INCREASE, $userActionLogActivityId);
                }
            }
            //剩余奖品数减一
            $prizeModel->reducePrizeCntLeft($prize['id']);
            $arr = array(
                'user_action_log_32_id' => $userActionLogActivityId,
                'prize_id' => $prize['id'],
                'activity_id' => $activityId,
                'prize_name' => $prize['name'],
                'user_name' => $userInfo['FirstName'],
                'uid' => $uid,
            );
            $winnerModel = new Activity_ActWinnerModel();
            //统计用户信息
            $arr['channel'] = $channel;
            $arr['user_first_name'] = $userInfo['FirstName'];
            if (Util::isIOSChannel()) {
                $arr['platform'] = '2';
            } else {
                $arr['platform'] = '1';
            }
            $arr['version'] = $version;
            $winnerModel->addWinner($arr);
            if ($activityId == 23) {//只针对瑜乐学院推送瑜小蜜 临时代码
                $code = self::$code[$prize['grade']];
                $pushTitle = '恭喜您中奖了';
//                $pushContent = "恭喜您获得美联盟瑜伽教练课程优惠兑换码 {$code}，用于抵扣美国瑜伽联盟IYT200小时瑜伽教练培训费，请您在2016年3月20日前兑换。\r\n如有问题请联系客服15109291795， 或者微信：1617055907\r\n美联盟瑜伽教练培训是全球最权威的瑜伽教练培训体系，毕业后将获得全球最被认可的瑜伽教练证书。\r\n\r\n不妨来看看吧！";
                $pushContent = "恭喜您在抽奖活动中获得“线下培训”送出的代金券，我们的工作人员随后将会电话联系您相关事宜，非常感谢您参加活动，祝一切顺利！";
                // 推送瑜小蜜
                $servicePushSend = new Service_Service_Push_Send([$uid], $pushTitle, $pushContent);
                $servicePushSend->setExtraParams(['link_type' => Library_Common::PUSH_LINK_TYPE_POST, 'obj_id' => 290404]);
                $servicePushSend->sendPush();
            }
        }
        return $result;
    }

    private function lotteryStrategy($uid, $activityId, $prizeList, $activity = array()) {
        $winnerModel = new Activity_ActWinnerModel();
        if ($activity['type'] == Library_Activity::ACTIVITY_TYPE_LOTTERY_DRAW_SCORE) {
            $winner = $winnerModel->getLimitWinnerByUidAndActivityId($uid, $activity);
        } else {
            $winner = $winnerModel->getWinnerByUidAndActivityId($uid, $activityId);
        }
        foreach ($prizeList as $key => &$prize) {
            if ($winner) {//已中过奖
                $prize['probability'] = 0;
            } else if ($prize['prize_cnt_left'] < 1) {//奖品没了
                $prize['probability'] = 0;
            } else if ($prize['internal_uids']) {
                $internalUids = explode(',', $prize['internal_uids']);
                if (in_array($uid, $internalUids)) {//内部作弊用户
                    $prize['probability'] = $this->_probabilityTotal;
                    $flag = $key;
                    break;
                }
            }
        }

        if (isset($flag)) {
            foreach ($prizeList as $key => &$one) {
                if ($key != $flag) {
                    $one['probability'] = 0;
                }
            }
        }

        return $prizeList;
    }

    //检查大转盘用户信息
    public function checkUserContactAction() {
        $userInfo = $this->checkUserLogin(true);
        if (empty($userInfo)) {
            $this->outPut('', '用户未登录', 2);
        }
        Log::trace('writeUser===>' . json_encode($_REQUEST));
        $uid = $userInfo['uid'];
        $activity_id = $this->get('activity_id', 0);
        DBC::requireTrue($activity_id != 0, '请填写活动id');
        $activityUserModel = new Activity_ActUserContactModel();
        if ($row = $activityUserModel->getUserInfoByActivityId($activity_id, $uid)) {
            $this->outPut($row, '', 1);
        }
        $this->outPut();
    }

    //大转盘填写用户信息
    public function writeUserContactAction() {
        Log::trace('writeUserContact===>' . json_encode($_REQUEST));
        $userInfo = $this->checkUserLogin(true);
        if (empty($userInfo)) {
            $this->outPut('', '用户未登录', 2);
        }
        $uid = $userInfo['uid'];
        $activity_id = $this->post('activity_id', 0);
        $name = $this->post('name', '');
        $telephone = $this->post('telephone', '');
        $address = $this->post('address', '');
        $channel = $this->post('channel', '');
        if (!$activity_id || !$name || !$telephone || !$address) {
            $this->outPut('', '数据不全', -1);
        }
        $activityUserModel = new Activity_ActUserContactModel();
        if ($row = $activityUserModel->getUserInfoByActivityId($activity_id, $uid)) {
            $contactContactData = array(
                'name' => $name,
                'telephone' => $telephone,
                'address' => $address,
                'update_time' => time()
            );
            $activityUserModel->update($contactContactData, array('activity_id' => $activity_id, 'uid' => $uid));
        } else {
            $contactContactData = array(
                'activity_id' => $activity_id,
                'uid' => $uid,
                'name' => $name,
                'telephone' => $telephone,
                'address' => $address,
                'status' => 1,
                'create_time' => time(),
                'update_time' => time()
            );
            $activityUserModel->addData($contactContactData);
        }
        $this->outPut();
    }

    //领奖信息提交接口
    public function postUserInfoAction() {
        Log::trace('postUserInfo===>' . json_encode($_REQUEST));
        $prizeId = $this->get('prize_id', '');
        $username = $this->post('username', '');
        $phone = $this->post('phone', '');
        $zipcode = $this->post('zipcode', '');
        $address = $this->post('address', '');

        if (!$prizeId || !$username || !$phone || !$zipcode || !$address) {
            $this->outPut('', '数据不全', -1);
        }

        $userInfo = $this->checkUserLogin(true);
        if (empty($userInfo)) {
            $this->outPut('', '用户未登录', 2);
        }
        $uid = $userInfo['uid'];

        $winnerModel = new Activity_ActWinnerModel();
        $winner = $winnerModel->getWinnerByUidAndPrizeId($uid, $prizeId);
        if (!$winner) {
            $this->outPut('', '很抱歉，您没有中奖', -1);
        }

        $arr = array(
            'id' => $winner['id'],
            'user_name' => $username,
            'phone' => $phone,
            'zip_code' => $zipcode,
            'address' => $address,
        );

        $winnerModel->updateWinner($arr);
        $this->outPut('', '', 0);
    }

    //获奖记录
    public function winnerListAction() {
        $activity_id = $this->get('activity_id', 0);
        $winnerModel = new Activity_ActWinnerModel();
        $result = $winnerModel->getWinnerByActivityId($activity_id);
        $this->outPut($result);
    }

    //瑜币商城抽奖记录
    public function activityRecordAction() {
        $userinfo = $this->checkUserLogin(true);
        $page = $this->request('page', 1);
        $pageSize = $this->request('page_size', 20);
        $winnerModel = new Activity_ActWinnerModel();
        $winnerList = $winnerModel->getWinnerListByUid4Page($userinfo['uid'], $page, $pageSize);

        if ($winnerList) {
            foreach ($winnerList as $winner) {
                $prizeIds[] = $winner['prize_id'];
            }
            $prizeModel = new Activity_ActPrizeModel();
            $prizeList = $prizeModel->getPrizeListByPrizeIds($prizeIds);
            $prizeDic = Util::array2Dic($prizeList, 'id');
            foreach ($winnerList as $key => &$one) {
                $prize = $prizeDic[$one['prize_id']];
                $one['prize_type'] = $prize['type'];
                $one['prize_name'] = $prize['name'];
                $one['prize_desc'] = $prize['desc'];
                $one['prize_image'] = $prize['image'];
                $one['date'] = Util::getCreateTime($one['create_time']);

                if ($prize['type'] == Library_Activity::PRIZE_ENTITY) {
                    $one['prize_name'] = $prize['desc'];
                    $one['prize_desc'] = '配送中';
                } else if ($prize['type'] == Library_Activity::PRIZE_POINTS) {
                    $one['prize_name'] = $prize['desc'] . '瑜币';
                    $one['prize_desc'] = '已到账';
                } else if ($prize['type'] == Library_Activity::PRIZE_CARD) {
                    //nothing
                }
            }
        }
        $this->outPut($winnerList);
    }

    // 2017-10-08 处理 苏斌 活动 新老用户拉新 新用户注册逻辑未修改 老用户自动发放（调用注册时候的发放接口）
    public function claimPrize($activity, $data) {
        //  前置条件重构到活动判断流程中，在判斷函數里斷言返回
        $this->activityModel->canJoin($data, $activity);

        $prizeList = (new Service_Service_Activity_Activity())->getActivityPrizeList($activity, $data['mobile']);

        $ret = [
            'status' => 0,
            'data' => [
                'result_page_bg_img' => $activity['result_page_bg_img']
            ]
        ];
        $prize_count = 0;
        $sendPrizeList = array();
        $prizeModel = new Activity_ActPrizeModel ();
        foreach ($prizeList as $prize) {
            // 是否有奖可发
            if ($prize ['prize_cnt'] > 0 && $prize ['prize_cnt_left'] < 1)
                continue;

            // 更新剩余奖品数量
            if ($prize ['prize_cnt'] > 0)
                $prizeModel->reducePrizeCntLeft($prize ['id']);

            $arr['uid'] = isset($data ['user'] ['uid']) ? $data ['user'] ['uid'] : '';
            $arr['user_first_name']= isset($data ['user'] ['nickName']) ? $data ['user'] ['nickName'] : '';
            $arr['activity_id']    = $activity ['id'];
            $arr['prize_id']       = $prize ['id'];
            $arr['prize_name']     = $prize ['name'];
            $arr['phone']          = $data ['mobile'];
            $arr['use_type']       = $prize ['use_type'];
            $arr['is_used']        = $prize ['use_type'] == Library_Activity::PRIZE_USE_TYPE_AUTO ? 0 : 1;
            $arr['has_pop_window'] = $activity['type'] == Library_Activity::ACTIVITY_TYPE_MOBLIE ? Library_Activity::ACTIVITY_POP_WINDOWS_YES : Library_Activity::ACTIVITY_POP_WINDOWS_NO;

            $winnerModel = new Activity_ActWinnerModel ();
            $winnerModel->addWinner($arr);
            $sendPrizeList[$prize_count] = $arr;
            $prize_count++;
            // 风控周期记录
            Activity_AmountLimitModel::recordPeriodStartTime($activity['amount_limit_id'], $data['mobile']);
        }

        // 神策上报
        $user = (new User_AccountInfoModel())->getUserByMobile($data['mobile']);
        $uid = !empty($data['user']['uid']) ? $data['user']['uid'] : 0;
        Util::eventTracking($uid, 'website_activity_received_gift', [
            'mobile' => $data['mobile'],
            'activity_id' => $activity['id'],
            'is_regist' => !empty($user),
        ]);
        if (empty($user) && !empty($activity['result_page_bg_img_new_people'])) {
            $ret['data']['result_page_bg_img'] = $activity['result_page_bg_img_new_people'];
        }

        DBC::requireTrue($prize_count != 0, '啊哦~你来晚了一步，奖品已经领取完了~', -1);
        // 处理老用户自动发放（调用注册时候的发放接口）20171018
        if ($prize['use_type'] == Library_Activity::PRIZE_USE_TYPE_AUTO && !empty($data ['user'])) {
            $winnerModel = new Activity_ActWinnerModel ();
            foreach ($sendPrizeList as $aw) {
                $prizeModel->sendPrize($aw ['activity_id'], $aw ['prize_id'], $data ['user']);
                $winnerModel->setUsed($aw ['id']);
            }
        }
        return $ret;
    }

    //拉新活动脚本
    public function scriptInviteLockListAction() {
        $activity_id = $this->get('activity_id', 0);
        $inviteUserModel = new Activity_InviteUserModel();
        $inviteUserModel->lockRank($activity_id);
    }

    //活动产品
    public function getActivityPayParamAction() {
        $deviceType = Util::getDtype();  //设备类型：1.android phone 2 iphone 3 iPad 4 android pad
        $payType = Library_Product::$iosPayMent;
        if ($deviceType == Library_Posts::DEVICE_ANDROID_PAD || $deviceType == Library_Posts::DEVICE_ANDROID_PHONE) {
            $payType = Library_Product::$andoidPayMent;
        }
        $data = array(
            'pay_type' => $payType,
            'source_type' => Library_WebOrder::SOURCE_TYPE_ACTIVITY, //web_order 7-活动
            'product_type' => Library_WebOrder::PAYMENT_ORDER_TYPE_VIP //会员支付
        );
        $this->outPut($data);
    }

    //用户2016年终数据
    public function userInfoIn2016Action() {
        $model = new Activity_ActivityFinalModel();
        $sid = $this->get('sid', 0);
        $r = $this->get('r', 0);
        $uid = $model->getUidByParam($sid, $r);
        $list = $model->getListFor2016($uid);
        $this->outPut($list);
    }

    /**
     * 用户2017年终数据展示
     * @param unknown $param
     * @author water
     * @since 2018年1月2日 下午3:28:53
     */
    public function userInfoIn2017Action() {
        $model = new Activity_ActivityFinalModel();
        $sid = $this->get('sid', 0);
        $r = $this->get('r', 0);
        $uid = $model->getUidByParam($sid, $r);
        $list = $model->getListFor2017($uid);
        $this->outPut($list);
    }

    /**
     * h5页面活动登陆
     *
     * @desc： 微信openid
     * @author : Oway
     */
    public function login4ActivityAction() {
        $loginType = $this->request('loginType', 0);
        $username = $this->post('username', '');
        $password = $this->post('password', '');
        $code = $this->get('code', ''); //微信码

        $userModel = new UserCenter_UserModel();
        if ($loginType < 3) {    //邮箱或者手机登陆
            //判断用户名和密码是否为空
            DBC::requireTrue(!empty($username) && !empty($password), '用户名或密码不能为空', 2);
            $usertype = 3;
            if (is_numeric($username)) {
                if (!Util::checkPhone($username)) {
                    $this->outPut(3, '手机号格式不正确');
                }
            } else {
                if (Util::checkEmail($username)) {
                    $usertype = 2;
                } else {
                    $this->outPut(3, '邮箱格式不正确');
                }
            }
            //获取用户信息
            $userinfo = $userModel->getUserInfo($username, $usertype);
            DBC::requireNotEmpty($userinfo, '用户信息不存在', 404);
            //检查密码是否正确
            if (($userinfo['Password'] && $userinfo['Password'] === $password) || ($userinfo['Password2'] && $userinfo['Password2'] === md5($password))) {
                //生成sid
                $sid = $userModel->genSessionId();

                $userinfo['sid'] = $sid;
                if ($usertype == 3) {
                    $userinfo['loginType'] = 1;
                } else {
                    //同步用户的粉丝数和关注数
                    $userinfo['loginType'] = 2;
                }
                $userModel->changeUserInfo(array('loginType' => $loginType), array('AccountId' => $userinfo['AccountId']));
            } else {
                $this->outPut(3, '密码错误');
            }
        } else {    //第三方登陆
            $activity_final_model = new Activity_ActivityFinalModel();
            switch ($loginType) {
                case 3 :    //QQ
                    $userinfo = $activity_final_model->qqLogin($code);
                    break;
                case 4 :    //微博
                    $userinfo = $activity_final_model->weiboLogin($code);
                    break;
                case 5 :    //  微信
                    $userinfo = $activity_final_model->weixinLogin($code);
                    break;
            }
            //生成sid
            $sid = $userModel->genSessionId();
            $userinfo['sid'] = $sid;
        }
        $userModel->changeUserInfo(array('loginType' => $loginType), array('AccountId' => $userinfo['AccountId']));
        $this->outPut(array('uid' => $userinfo['AccountId'], 'sid' => $userinfo['sid']));
    }

    //通过真实sid加密获得假的sid
    public function getAsidBySidAction() {
        $userInfo = $this->checkUserLogin(true);
        $r = rand(1, 10);
        $sid = base64_encode($userInfo['uid'] << $r);
        $this->outPut(array('sid' => $sid, 'r' => $r));
    }

    //达人活动-首页
    public function talentsIndexAction() {
        $sid = $this->get('sid', 0);
        $activity_id = $this->get('activity_id', 0);
        $other_count = $this->get('other_count', 3);
        DBC::requireNotEmpty($activity_id, '参数错误');
        $talentsModel = new Activity_ActivityTalentsModel();
        $info = $talentsModel->getInfoByActivityId($activity_id, $other_count);
        $userModel = new UserCenter_UserModel();
        $uid = $userModel->getUidBySid($sid);
        $is_apply = $talentsModel->checkUserApply($activity_id, $uid);
        $info['is_apply'] = $is_apply ? 0 : 1;
        $this->outPut($info);
    }

    //达人活动-报名
    public function talentsApplyAction() {
        $activity_id = $this->post('activity_id', 0);
        DBC::requireNotEmpty($activity_id, '参数错误');
        $userInfo = $this->checkUserLogin(true);
        //>>1.检验活动状态
        $talentsModel = new Activity_ActivityTalentsModel();
        $talentsInfo = $talentsModel->getTalentsInfo($activity_id);
        DBC::requireTrue($talentsInfo['activity_status'] == Library_Activity::ACTIVITY_TALENTS_STATUS_APPLY_ING, '报名已经结束啦，敬请期待入选结果！');
        //>>2.检测该用户是否已经报名
        $is_apply = $talentsModel->checkUserApply($activity_id, $userInfo['uid']);
        DBC::requireTrue($is_apply, '亲，你已经报过名啦，不要重复申请哦~~~');
        //>>3.报名
        $result = $talentsModel->apply($activity_id, $userInfo);
        if (!$result) {
            $this->outPut(999999);
        }
        $this->outPut(array('data' => 'success'));
    }

    //达人活动-投票
    public function talentsVoteAction() {

        $activity_id = $this->post('activity_id', 0);
        DBC::requireNotEmpty($activity_id, '参数错误');
        $uid = $this->post('uid', 0);
        DBC::requireNotEmpty($activity_id, '参数错误');

        //检查用户信息 & 投票渠道
        $sid = $this->post('sid', 0);   //用户uid，在app内投票
        $open_id = $this->post('openid', "");  //微信openid,在微信内投票
        if (empty($sid) && empty($open_id)) {
            DBC::requireNotEmpty(0, '请在每日瑜伽App 或 微信中进行投票哦 ^_^...');
        }
        if (!empty($sid) && empty(!$open_id)) {
            DBC::requireNotEmpty(0, '参数错误');
        }

        if(!empty($open_id)) {
            $CryptAES = new CryptAES(Library_Thirdparty::APP_WEIXIN_SECRET_KEY);
            $open_id = $CryptAES->decryptWithSSL($open_id);

            $publicHelps = new Service_Service_Wechat_PublicHelps();
            $wxUserInfo = $publicHelps->getWXUserInfo($open_id);
            if(empty($wxUserInfo)) {
                DBC::requireTrue(false, '请在每日瑜伽App 或 微信中进行投票哦 ^_^..');
            }
            DBC::requireTrue($open_id, '请在每日瑜伽App 或 微信中进行投票哦 ^_^..');
        }

        $userInfo = [];
        if(!empty($sid)) {
            $userInfo = $this->checkUserLogin(true);
        }

        //1.检验活动状态
        $talentsModel = new Activity_ActivityTalentsModel();
        $talentsInfo = $talentsModel->getTalentsInfo($activity_id);
        DBC::requireNotEmpty($talentsInfo, '活动不存在');
        if ($talentsInfo['activity_status'] < Library_Activity::ACTIVITY_TALENTS_STATUS_VOTE_ING) {
            $this->outPut(1, '亲，投票时间还没开始，请稍等哦~');
        } elseif ($talentsInfo['activity_status'] > Library_Activity::ACTIVITY_TALENTS_STATUS_VOTE_ING) {
            $this->outPut(2, '投票已经结束啦，敬请期待评选结果！');
        }

        //获得分享总次数
        $share_count = $talentsModel->getShareVoteCount($userInfo['uid'], $activity_id,$open_id);

//        //>>2.检查用户投票次数是否已经超过最大值
//        $is_out_max_vote = $talentsModel->outMaxVote($userInfo['uid'],$talentsInfo['vote_max_count'],$activity_id,$share_count);
//        DBC::requireTrue($is_out_max_vote,'您已经超过最大投票次数啦～');
        //>>3.检查用户今天投票次数是否已经超过




        $is_out_max_vote_daily = $talentsModel->outMaxVoteDaily($userInfo['uid'], $talentsInfo['vote_base_count_daily'], $activity_id, $share_count,$open_id);


        if($share_count < $talentsInfo["vote_max_count"] && empty($open_id)) {
            DBC::requireTrue($is_out_max_vote_daily, '分享活动可增加投票机会 快去分享吧~');
        } else {
            DBC::requireTrue($is_out_max_vote_daily, '今天投票已达上限，快去下载“每日瑜伽”app，每天可投3票哦');
        }


//        //>>4.检查该用户是否已经给该用户透过票
//        $is_vote_uid = $talentsModel->isVoteToUid($userInfo['uid'],$uid,$activity_id);
//        DBC::requireTrue($is_vote_uid,'你已经给她(他)投过票啦，请给其他用户也投一张吧~');
        //>>5.记录数据
        //计算剩余投票次数
        $count = $talentsModel->countMaxVoteDaily($userInfo['uid'], $talentsInfo['vote_base_count_daily'], $activity_id, $talentsInfo["vote_max_count"],$open_id);
        $rs = $talentsModel->createVoteInfo($activity_id, $userInfo['uid'], $uid,$open_id);
        if (!$rs) {
            $this->outPut(999999,$count);
        }
        $this->outPut(['count' => $count - 1,'share_left_count' => $talentsInfo["vote_max_count"] - $share_count]);
    }

    //达人活动-分享
    public function talentsShareAction() {
        $activity_id = $this->post('activity_id', 0);
        DBC::requireNotEmpty($activity_id, '参数错误');
        $userInfo = $this->checkUserLogin(true);
        $talentsModel = new Activity_ActivityTalentsModel();
        $rs = $talentsModel->createShareData($userInfo['uid'], $activity_id);
        if (!$rs) {
            $this->outPut(999999);
        }
        $this->outPut();
    }

    /**
     * 母亲节活动
     * @author water
     * @since 2018/5/3 17:09
     */
    public function activityShareAction() {
        if (!Util::checkSign($_REQUEST, Library_ParamsCheck::NEED_CHECK_ON)) {
            // 2018-02-08 11:55:03 庞晓楠 修改 返回403
            Util::ResultHTTPStatusCode(Library_HTTPStatusCode::FORBIDDEN);
        }
        $today=date('YmdHis');
        if (Library_Activity::ACTIVITY_SHARE_MOTHER_START_TIME>$today&&$today>Library_Activity::ACTIVITY_SHARE_MOTHER_END_TIME){
            //2019/9/4 17:53 tlqiao 原来表达式1！=1 直接传false
            DBC::requireTrue(false,'活动已过期');
        }
        $userInfo = $this->checkUserLogin(true);
        $Activity_ActivityUserRecordModel=new Activity_ActivityUserRecordModel();
        $param=array(
            'uid'=>$userInfo['uid'],
            'activity_id'=>Library_Activity::ACTIVITY_SHARE_MOTHER_DAY
        );
        $getActivityUserRecordInfo=$Activity_ActivityUserRecordModel->getActivityUserRecord($param);
        if (!$getActivityUserRecordInfo){
            $userRecordInfo=$Activity_ActivityUserRecordModel->addActivityUserRecord($param);
            //2019/9/4 17:53 tlqiao 原来表达式1！=1 直接传false
            if (!$userRecordInfo) {
                DBC::requireTrue(false, '数据错误请联系客服');
            }
            $service = new Service_Api_Coupon_Gift();
            $data = array(
                'gift_id' => Library_Activity::ACTIVITY_SHARE_GIFT_ID,
                'uid' => $userInfo['uid']
            );
            $reslut = $service->useGift($data);
            if ($reslut['errno'] != 0) {
                Log::trace('collect_cards_gift_packs===' . json_encode($reslut));
            }
        }else{
            DBC::requireTrue(false,'您已领取过礼包');
        }
        $this->outPut();
    }

    /**
     * @desc 获取活动弹窗
     */
    public function getActivityWindowListAction() {
        $result = [
            'pop_window_list' => [],
        ];

        // 获取用户
        $activityIDList = $needUpdateActivityIDList = [];
        $phone = $this->request('phone', 0);
        $userJoinActivityList = (new Service_Service_Activity_GiftActivity())->getUserJoinActivityList($phone);
        foreach ($userJoinActivityList as $userJoinActivityInfo) {
            $activityIDList[] = $userJoinActivityInfo['activity_id'];
        }

        if (count($activityIDList) == 0) {
            $this->outPut($result);
        }
        $activityList = (new Service_Service_Activity_GiftActivity())->getActivityInfoBatch($activityIDList);
        foreach ($userJoinActivityList as $userJoinActivityInfo) {
            if (!isset($activityList[$userJoinActivityInfo['activity_id']])) {
                continue;
            }

            // 用户领取奖励至注册时间超过7天则不弹窗（与领取奖励逻辑保持一致）
            if ((time() - $userJoinActivityInfo['create_time']) > 7 * 24 * 3600) {
                continue;
            }

            $data = json_decode($activityList[$userJoinActivityInfo['activity_id']]['content']);
            if (!$data) {
                continue;
            }
            $result['pop_window_list'][] = $data;
            $needUpdateActivityIDList[] = $userJoinActivityInfo['id'];
        }

        // 更新用户参加活动弹窗状态
        if (count($needUpdateActivityIDList)) {
            (new Activity_ActWinnerModel)->updatePopWindowStatusBatch($needUpdateActivityIDList);
        }

        $this->outPut($result);
    }
}
