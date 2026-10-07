import { Link, useOutletContext } from "react-router-dom";

const FIELDS = [
  ["first_name", "نام"],
  ["last_name", "نام خانوادگی"],
  ["email", "پست الکترونیک"],
  ["mobile", "شماره تلفن همراه"],
  ["zipcode", "کد پستی"],
  ["back_money", "روش بازگرداندن پول من"],
  ["age", "سن"],
  ["national_code", "کد ملی"],
  ["card_number", "شماره کارت"],
  ["iban", "شماره شبا"],
];

export default function ProfilePage() {
  const { profile } = useOutletContext();

  return (
    <div className="row">
      <div className="col-lg-12">
        <header className="card-header">
          <h3 className="card-title">
            <span>اطلاعات حساب کاربری</span>
          </h3>
        </header>
        <div className="content-section default">
          <div className="row">
            {FIELDS.map(([name, label]) => (
              <div className="col-sm-12 col-md-6" key={name}>
                <p>
                  <span className="title">{label} :</span> <span>{profile[name] || "-"}</span>
                </p>
              </div>
            ))}
            {!profile.is_complete && (
              <div className="col-12">
                <p className="txt_note">
                  <i className="fa fa-info" aria-hidden="true" /> اطلاعات شما کامل نیست. برای تکمیل سفارش‌ها، پروفایل خود را کامل کنید.
                </p>
              </div>
            )}
            <div className="col-12 text-center">
              <Link to="/account/edit" className="btn btn-main-masai big_btn">
                ویرایش
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
