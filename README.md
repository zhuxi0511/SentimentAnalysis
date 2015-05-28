# 有监督机器学习平台

### 总体介绍

本有监督机器学习平台期望解决一类以特征向量为主要输入数据的有监督机器学习问题

### 命令参数

	./analysis.py [--preprocess] [--train] [--predict] [--combine] [--check_algo] config_file

* [--preprocess] [--train] [--predict] [--combine] [--check_algo]表示控制流程，分别为预处理，训练，预测，综合处理，模型校验流程。

* config_file表示配置文件所在地址，传入平台后会自动解析配置文件中的相关设置自动进行对应的控制流程。

### 配置文件说明

[ALGORITHM]
		
	algorithm_dir：算法库目录
	algorithm：选用进行学习的算法

[DATA]

	data_dir：训练及测试数据所在目录
			  在data目录中原始训练及测试数据需要以 *.train.raw和 *.test.raw的格式命名，平台会自动合并所有训练以及测试数据。
	model_dir：模型保存目录
	log_dir：日志保存目录，平台会自动以运行开始时间命名对应日志
	output_dir：预测结果保存目录
	
[PREPROCESS]
	
	pretreat_module：公共信息预处理模块名
	extract_module：特征抽取处理模块名

[TRAIN]
	
	train_file：特定训练数据（默认ALL）
	model_name：指定训练得到的模型保存的名字（默认AUTO）

[PREDICT]
	
	test_file：特定预测数据（默认ALL）
	test_model：预测所用模型名字（默认AUTO）

[OTHER]
	
	send_mail_list：错误信息邮寄地址
	
一个典型的配置文件如下：

	[ALGORITHM]
	algorithm_dir=~/weibo/algorithm
	algorithm=maxent_baseline
	
	[DATA]
	data_dir=~/weibo/data
	model_dir=~/weibo/model
	log_dir=~/weibo/log
	output_dir=~/weibo/output
	
	[PREPROCESS]
	pretreat_module=maxent_pretreat
	extract_module=word_list emotion_word syntax sentence_length
	
	[TRAIN]
	train_file=ALL
	model_name=AUTO
	
	[PREDICT]
	test_file=ALL
	test_model=AUTO
	
	[OTHER]
	send_mail_list=zhuxi910511@163.com

### 算法接口说明

为了保证整个平台的开发性以及灵活性，平台为算法模块提供了实现接口，若要实现不同的算法，只要实现一个对应的算法类，并根据平台的规定实现其中的init(), train(train_file,model_file), predict(test_file, model_file, output_file)这三个接口并接受平台规定的数据标准即可。

为了适应各种不同算法流程的需求，对于无法区分train，predict流程的算法，平台提供了combine(train_file, test_file, output_file)接口，可以直接完成从数据到输出的工作。

以下是一个典型的算法模块：

	#!/user/bin/env python
	# coding: utf-8
	
	from maxent import MaxentModel
	
	class MaxentBaseline:
	
	    def __init__(self):
	        self.maxent = MaxentModel()
	
	    def train(self, train_file, model_file):
	        f = open(train_file)
	        self.maxent.begin_add_event()
	        for line in f.readlines():
	            item_id, tag, features = line.strip().split('\t')
	            features = map(lambda x:x.split(':'), features.split(' '))
	            features = map(lambda x:(x[0], float(x[1])), features)
	            if tag != '0':
	                self.maxent.add_event(features, tag, 4)
	            else:
	                self.maxent.add_event(features, tag, 1)
	        self.maxent.end_add_event()
	
	        self.maxent.train(30, 'lbfgs')
	        self.maxent.save(model_file)
	
	    def predict(self, test_file, model_file, output_file):
	        self.maxent.load(model_file)
	        f = open(test_file)
	        of = open(output_file, 'w')
	        for line in f.readlines():
	            item_id, tag, features = line.strip().split('\t')
	            features = map(lambda x:x.split(':'), features.split(' '))
	            features = map(lambda x:(x[0], float(x[1])), features)
	            max_tag = self.maxent.eval_all(features)[0][0]
	            of.write('%s\t%s\n' % (item_id, max_tag))
	        of.close()
	        f.close()

将此算法模块放入配置文件中的algorithm_dir下，并用algorithm=maxent_baseline指定即可使用。

**tips**：算法模块的命名需要符合PEP 8标准，即文件名使用lower_case_with_underscores风格，类名使用CapitalizedWords风格。在这里文件名为maxent_baseline，类名为MaxentBaseline，由于自动载入的关系，请将文件名与类名**内容保持一致**。

### 预处理模块说明

此工具的预处理流程分为pretreat和extract部分。extract抽取得到的特征会通过平台统一编号并合并结果，用于算法模块的训练以及预测过程。

pretreat部分用于预处理数据获取public_resource，用户可以自定义一个函数来完成这部分的功能，其基本形式为：

	def maxent_pretreat(item_info):
		...
		return public_resource

extract部分用于提取item的特征，可以指定多个函数一起完成这部分功能，其基本形式为：

	def word_list(item_info, public_resource): 
		...
        return item_feature_list

* item_feature_list是一个列表，每一个元素值为(item,feature)。<br/>
* item_info为读入的原始数据，其结构在之后的数据标准中。<br/>
* public_resource为用户自定义的资源结构，可以由用户自己自由使用

pretreat和extract所使用的模块函数需要由用户实现，分别将其放入`config['algorithm_dir']/pre/pretreat.py`和`config['algorithm_dir']/pre/extract.py`，然后由配置文件指定即可调用。这部分内容具体设置可参考[工程简单例子](https://github.com/zhuxi0511/slt_sample_dir)

### 数据接口标准

为了保证各个模块在数据交接时的一致性，平台通过统一数据接口以及纯文本传递来实现多种处理库之间的协调运作。实现平台通用化，高灵活的目标。

原始输入数据item_info保存结构：
	
	{ item_id1:{content:xx,tag:xx},
	  item_id2:{content:xx,tag:xx},… }
	  
item_info从文件中读入的格式为：
	
	item_id[\t]content[\t]tag

这个数据为每个item语料的原始数据，包括每个item语料的id，原始内容以及标准标注。<br/>
**tips**:此数据作为原始输入数据，需要以`*.train.raw`，`*.test.raw`为文件名存储在配置文件的data_dir目录下。

***

数据特征向量存储结构：

	[ {item_id:xx,tag:xx,value:{feature1:value1,feature2:value2,…,}},
	  {item_id:xx,tag:xx,value:{feature1:value1,feature2:value2,…,}}, … ]
	  
特征向量写入到文件后的格式为：
	
	item_id[\t]tag[\t]feature1:value1[ ]feature2:value2[ ] …

**tips**：此文件数据格式为训练及预测过程中的输入文件train_file和test_file的格式，用户实现的算法需要以此格式为标准解析输入数据。

***

feature_dict特征词典保存结构：
	
	{ feature1:feature_id1, feature2:feature_id2 }

feature_dict特征词典写入到文件后的格式为

	feature[\t]feature_id
	
***

output_file输出文件格式

	item_id[\t]tag
	
**tips**:此文件为预测结果输出文件格式，用于平台自动计算预测结果的准确率召回率以及F值。

***

model数据结构：

model结构由于algorithm模块算法不同，由不同算法自行决定，平台在生产model时会记录相应的算法信息并默认按照时间起名保存在指定model目录中，保证为每个预测流程中使用的算法不会错乱。

### 运行时说明

[--preprocess] [--train] [--predict]流程分别对应预处理，训练，以及预测流程：

* 在preprocess流程中，平台会将所有`*.train.raw`，`*.test.raw`文件处理成保存特征向量结构的`*.train`，`*.test`文件。



* 在train流程中，平台会根据配置文件中的train_file确定所需训练的文件（默认为所有`*.train`文件），并根据model_name值保存获得的模型（默认为命名为运行时刻），与模型一起保存的还有训练所用的算法以及训练数据名。同时，运行所有的配置文件也会拷贝到模型目录中，以便于复现实验。
* 在predict流程中，平台会根据配置文件中的test_file确定所需预测的文件（默认为所有`*.test`文件），并根据test_model值读取进行预测所要使用的model（默认为上一次train流程所获得的model），最终输出结果到output_dir目录，同时保存model信息，预测所用数据名，和自动评价的准确率召回率F值结果。

