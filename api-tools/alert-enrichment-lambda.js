var aws = require('aws-sdk');
var http = require('https');
var ec2 = new aws.EC2({region: ''}); //AWS region name, i.e. us-east-1

var cluster = ''; //Hostname of your cluster, i.e. customer.portal.jask.io
var username = ''; //Username to use when authenticating to the Trident API
var api_key = ''; //API key to use when authenticating to the Trident API

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

var instanceMeta = {};

function saveToAsset(instanceMeta) {
  var data = JSON.stringify({'AWS': instanceMeta});
  console.log('updating asset metadata: ' + data);
  var options = {
    host: cluster,
    port: 443,
    path: '/api/asset/' + instanceMeta['public_ip'] + '/metadata?username=' + username + '&api_key=' + api_key,
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data)
    }
  }
  var req = http.request(options, function(res) {
    res.setEncoding('utf8');
  });
  req.write(data);
  req.end();
  req.on('error', function(e) {
    console.error(e);
  });
};

function addAmiMeta(instanceMeta) {
  var params = {ImageIds: [ instanceMeta['ami_id'] ]};
  ec2.describeImages(params, function(err, data) {
    instanceMeta['ami_name'] = data['Images'][0]['Name'];
    instanceMeta['ami_description'] = data['Images'][0]['Description'];
    console.log(JSON.stringify(instanceMeta));
    saveToAsset(instanceMeta);
  });
};

function findInstanceMeta(instanceIp) {
  console.log('instance ip is ' + instanceIp);
  ec2.describeInstances({
    Filters: [
      {
        Name: 'ip-address',
        Values: [
          instanceIp
        ]
      }
    ]
  }, function(err, data) {
    console.log(JSON.stringify(data));
    var instance = data['Reservations'][0]['Instances'][0];
    instanceMeta['ami_id'] = instance['ImageId'];
    instanceMeta['hostname'] = instance['PrivateDnsName'];
    instanceMeta['type'] = instance['InstanceType'];
    instanceMeta['public_ip'] = instanceIp;
    instanceMeta['private_ip'] = instance['PrivateIpAddress'];
    instanceMeta['availabilityZone'] = instance['Placement']['AvailabilityZone'];
    addAmiMeta(instanceMeta);
  });
};

exports.handler = (event, context, callback) => {
  var msg = JSON.parse(event['Records'][0]['Sns']['Message']);
  console.log('Got message: ' + JSON.stringify(msg));
  var assetIp = msg['asset_ip'];
  findInstanceMeta(assetIp);
};

