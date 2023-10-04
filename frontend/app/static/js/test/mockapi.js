// Helper function
import { mockhandlers as loginhandlers } from "./mocks/mocklogin.js"
import { mockhandlers as profilehandlers } from "./mocks/mockprofile.js";
import { mockhandlers as deletehandlers } from "./mocks/mockDeleteAccount.js";
import { mockhandlers as forgotpasswordHandlers } from "./mocks/mockforgotpassword.js";
import { mockhandlers as validTokenHandlers } from "./mocks/mockvalidtoken.js";
import { mockhandlers as resetPasswordHandlers } from "./mocks/mockresetpassword.js";
var mockhandlers = [];
mockhandlers.push(...loginhandlers,
                  ...profilehandlers,
                  ...deletehandlers,
                  ...forgotpasswordHandlers,
                  ...validTokenHandlers,
                  ...resetPasswordHandlers);

var mockjaxhandlers = $.mockjax(
    mockhandlers
);