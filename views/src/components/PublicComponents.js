import React from 'react';
import "../scss/index.scss";

const handlerInputChangeContext = React.createContext();  //用于将父组件的input标签的change事件处理函数传递到底层dom上
                                                          //处理函数根据dom的id更新父组件state中对应的key(与dom id相同)

class FormInput extends React.Component {
  static contextType = handlerInputChangeContext;
  render() {
    const id          = this.props.id ? this.props.id:"exampleInputEmail1";
    const type        = this.props.type ? this.props.type : "text";
    const lable       = this.props.label;
    const placeholder = this.props.placeholder ? this.props.placeholder:"name@example.com";
    const help        = this.props.help ? this.props.help:"";
    return (
      <div className="form-group">
        <label htmlFor={id}>{lable}</label>
        <input type={type} className="form-control" id={id} aria-describedby="emailHelp"
               placeholder={placeholder} onChange={(e) => this.context( e,id)}/>
          <small id="emailHelp" className="form-text text-muted">{help}</small>
      </div>
    );
  }
}


export {handlerInputChangeContext, FormInput}