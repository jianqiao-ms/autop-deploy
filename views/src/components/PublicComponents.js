import React from 'react';
import "../scss/index.scss";

class FormInputEmail extends React.Component {
  render() {
    const id = this.props.id ? this.props.id:"exampleInputEmail1";
    const lable = this.props.label;
    const placeholder = this.props.placeholder ? this.props.placeholder:"name@example.com";
    const help = this.props.help ? this.props.help:"";
    return (
      <div className="form-group">
        <label htmlFor={id}>{lable}</label>
        <input type="email" className="form-control" id={id} aria-describedby="emailHelp"
               placeholder={placeholder}/>
          <small id="emailHelp" className="form-text text-muted">{help}</small>
      </div>
    );
  }
}

class FormInputText extends React.Component {
  render() {
    const id = this.props.id ? this.props.id:"exampleInputText1";
    const lable = this.props.label ? this.props.label:"";
    const placeholder = this.props.placeholder ? this.props.placeholder:"";
    const help = this.props.help ? this.props.help:"";
    return (
      <div className="form-group">
        <label htmlFor={id}>{lable}</label>
        <input type="text" className="form-control" id={id} aria-describedby="textHelp"
               placeholder={placeholder}/>
          <small id="textHelp" className="form-text text-muted">{help}</small>
      </div>
    );
  }
}

class FormInputPassword extends React.Component {
  render() {
    const id = this.props.id ? this.props.id:"exampleInputPassword1";
    const lable = this.props.label ? this.props.label:"Password";
    const placeholder = this.props.placeholder ? this.props.placeholder:"password";
    return (
      <div className="form-group">
        <label htmlFor={id}>{lable}</label>
        <input type="password" className="form-control" id={id} placeholder={placeholder} />
      </div>
    );
  }
}

export {FormInputEmail, FormInputText, FormInputPassword}